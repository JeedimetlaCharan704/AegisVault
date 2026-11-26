// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./InvariantGuard.sol";
import "./interfaces/IStrategy.sol";

/**
 * @title AegisVault
 * @notice Autonomous AI-Guarded ERC-4626 Yield Vault with Invariant Guardrails
 * @dev Combines tokenized yield vault architecture with dual-role AI execution:
 *      - Quant Agent: Optimizes yield and rebalances capital within invariant bounds
 *      - Sentinel Agent: Real-time emergency de-risking when anomalies or depegs occur
 */
contract AegisVault {
    string public name = "Aegis AI Guarded Vault";
    string public symbol = "agUSDC";
    uint8 public constant decimals = 6;

    // Underlying asset (e.g. USDC)
    address public immutable asset;
    InvariantGuard public immutable guard;
    address public owner;
    address public quantAgent;
    address public sentinelAgent;

    // ERC-20 / ERC-4626 Accounting
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    // Strategy tracking
    address[] public activeStrategies;
    mapping(address => bool) public isStrategyActive;
    mapping(address => uint256) public strategyAllocations;

    bool public paused;

    // Events
    event Deposit(address indexed sender, address indexed owner, uint256 assets, uint256 shares);
    event Withdraw(address indexed sender, address indexed receiver, address indexed owner, uint256 assets, uint256 shares);
    event RebalanceExecuted(address indexed fromStrategy, address indexed toStrategy, uint256 amount);
    event EmergencyDeRiskExecuted(address indexed compromisedStrategy, uint256 recoveredAssets, string reason);
    event AgentRolesUpdated(address indexed quantAgent, address indexed sentinelAgent);
    event VaultPaused(bool status);

    // Errors
    error Unauthorized();
    error VaultIsPaused();
    error InsufficientBalance();
    error InvalidAmount();
    error StrategyNotFound();
    error TransferFailed();

    modifier onlyOwner() {
        if (msg.sender != owner) revert Unauthorized();
        _;
    }

    modifier onlyAgent() {
        if (msg.sender != quantAgent && msg.sender != owner) revert Unauthorized();
        _;
    }

    modifier onlySentinelOrAgent() {
        if (msg.sender != sentinelAgent && msg.sender != quantAgent && msg.sender != owner) revert Unauthorized();
        _;
    }

    modifier whenNotPaused() {
        if (paused) revert VaultIsPaused();
        _;
    }

    constructor(address _asset, address _guard) {
        owner = msg.sender;
        asset = _asset;
        guard = InvariantGuard(_guard);
    }

    function setAgents(address _quantAgent, address _sentinelAgent) external onlyOwner {
        quantAgent = _quantAgent;
        sentinelAgent = _sentinelAgent;
        emit AgentRolesUpdated(_quantAgent, _sentinelAgent);
    }

    function setPaused(bool _status) external onlyOwner {
        paused = _status;
        emit VaultPaused(_status);
    }

    function addStrategy(address strategy) external onlyOwner {
        require(!isStrategyActive[strategy], "Strategy already added");
        isStrategyActive[strategy] = true;
        activeStrategies.push(strategy);
    }

    // --- ERC-4626 Core Accounting ---

    function totalAssets() public view returns (uint256 total) {
        // Vault liquid reserve
        total = IERC20Minimal(asset).balanceOf(address(this));
        // Add assets deployed in active strategies
        for (uint256 i = 0; i < activeStrategies.length; i++) {
            address strat = activeStrategies[i];
            if (isStrategyActive[strat]) {
                total += IStrategy(strat).totalAssets();
            }
        }
    }

    function convertToShares(uint256 assets) public view returns (uint256) {
        uint256 supply = totalSupply;
        uint256 total = totalAssets();
        if (supply == 0 || total == 0) return assets;
        return (assets * supply) / total;
    }

    function convertToAssets(uint256 shares) public view returns (uint256) {
        uint256 supply = totalSupply;
        if (supply == 0) return shares;
        return (shares * totalAssets()) / supply;
    }

    function deposit(uint256 assets, address receiver) external whenNotPaused returns (uint256 shares) {
        if (assets == 0) revert InvalidAmount();
        shares = convertToShares(assets);

        bool success = IERC20Minimal(asset).transferFrom(msg.sender, address(this), assets);
        if (!success) revert TransferFailed();

        totalSupply += shares;
        balanceOf[receiver] += shares;

        guard.updateDrawdownMonitor(totalAssets());
        emit Deposit(msg.sender, receiver, assets, shares);
    }

    function withdraw(uint256 assets, address receiver, address _owner) external returns (uint256 shares) {
        if (assets == 0) revert InvalidAmount();
        shares = convertToShares(assets);

        if (msg.sender != _owner && allowance[_owner][msg.sender] != type(uint256).max) {
            uint256 allowed = allowance[_owner][msg.sender];
            if (allowed < shares) revert InsufficientBalance();
            allowance[_owner][msg.sender] = allowed - shares;
        }

        if (balanceOf[_owner] < shares) revert InsufficientBalance();
        balanceOf[_owner] -= shares;
        totalSupply -= shares;

        // Ensure sufficient liquid reserve in vault, otherwise withdraw from strategies
        uint256 liquid = IERC20Minimal(asset).balanceOf(address(this));
        if (liquid < assets) {
            uint256 needed = assets - liquid;
            _pullFromStrategies(needed);
        }

        bool success = IERC20Minimal(asset).transfer(receiver, assets);
        if (!success) revert TransferFailed();

        guard.updateDrawdownMonitor(totalAssets());
        emit Withdraw(msg.sender, receiver, _owner, assets, shares);
    }

    // --- Autonomous Agent Rebalancing (Quant Agent) ---

    /**
     * @notice Rebalances capital from one strategy to another or from reserve to a strategy
     * @dev Strictly validates InvariantGuard rules before moving any token
     */
    function rebalance(
        address fromStrategy,
        address toStrategy,
        uint256 amount,
        uint256 expectedMinReceived,
        uint256 estimatedOutput
    ) external onlyAgent whenNotPaused {
        uint256 total = totalAssets();
        uint256 currentTargetAmount = toStrategy == address(0) 
            ? IERC20Minimal(asset).balanceOf(address(this)) 
            : IStrategy(toStrategy).totalAssets();

        // 1. Enforce mathematical invariant guardrails
        guard.validateRebalance(
            total,
            toStrategy,
            currentTargetAmount,
            amount,
            expectedMinReceived,
            estimatedOutput
        );

        // 2. Withdraw from source
        if (fromStrategy != address(0)) {
            require(isStrategyActive[fromStrategy], "Source not active");
            IStrategy(fromStrategy).withdraw(amount, address(this));
        }

        // 3. Deposit into destination
        if (toStrategy != address(0)) {
            IERC20Minimal(asset).approve(toStrategy, amount);
            IStrategy(toStrategy).deposit(amount);
        }

        guard.updateDrawdownMonitor(totalAssets());
        emit RebalanceExecuted(fromStrategy, toStrategy, amount);
    }

    // --- Emergency Sentinel Defense (Threat Sentinel Agent) ---

    /**
     * @notice Emergency action called by Sentinel Agent when flash-loan anomaly, hack, or depeg is detected
     * @dev Bypasses normal allocation caps to immediately salvage 100% of capital back to liquid reserve
     */
    function emergencyDeRisk(
        address compromisedStrategy,
        string calldata reason
    ) external onlySentinelOrAgent returns (uint256 recovered) {
        require(isStrategyActive[compromisedStrategy], "Strategy not active");

        uint256 strategyBalance = IStrategy(compromisedStrategy).totalAssets();
        if (strategyBalance > 0) {
            recovered = IStrategy(compromisedStrategy).withdraw(strategyBalance, address(this));
        }

        // Delist the compromised strategy to prevent further allocation
        isStrategyActive[compromisedStrategy] = false;

        emit EmergencyDeRiskExecuted(compromisedStrategy, recovered, reason);
    }

    function _pullFromStrategies(uint256 needed) internal {
        uint256 pulled = 0;
        for (uint256 i = 0; i < activeStrategies.length && pulled < needed; i++) {
            address strat = activeStrategies[i];
            if (isStrategyActive[strat]) {
                uint256 bal = IStrategy(strat).totalAssets();
                if (bal > 0) {
                    uint256 toPull = (needed - pulled) > bal ? bal : (needed - pulled);
                    pulled += IStrategy(strat).withdraw(toPull, address(this));
                }
            }
        }
    }
}

interface IERC20Minimal {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
}
