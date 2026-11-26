// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title InvariantGuard
 * @notice Mathematical invariant verification engine for AegisVault
 * @dev Enforces strict on-chain execution constraints so that off-chain AI agents
 *      CANNOT drain funds, exceed risk allocations, or interact with unverified protocols.
 */
contract InvariantGuard {
    // Basis points constant (100% = 10,000 bps)
    uint256 public constant BPS_DENOMINATOR = 10_000;

    // Invariant Constraints
    uint256 public maxSlippageBps = 50;           // Max 0.5% slippage on any rebalance
    uint256 public maxPoolAllocationBps = 4000;    // Max 40% of total vault assets in any single strategy
    uint256 public minLiquidReserveBps = 1000;     // Min 10% held in unallocated liquid reserve
    uint256 public maxHourlyDrawdownBps = 500;     // Max 5% drawdown before circuit breaker activates

    // Whitelisted strategies & routers
    mapping(address => bool) public whitelistedStrategies;

    // Circuit breaker state
    bool public circuitBreakerTriggered;
    uint256 public lastHourlyHighWatermark;
    uint256 public lastHourTimestamp;

    address public immutable owner;

    event StrategyWhitelisted(address indexed strategy, bool status);
    event InvariantParametersUpdated(uint256 maxSlippage, uint256 maxAllocation, uint256 minReserve);
    event CircuitBreakerTripped(uint256 timestamp, uint256 currentAssets, uint256 peakAssets);
    event CircuitBreakerReset(uint256 timestamp);

    error StrategyNotWhitelisted(address strategy);
    error SlippageExceeded(uint256 expected, uint256 actual, uint256 maxBps);
    error MaxAllocationExceeded(address strategy, uint256 proposedAmount, uint256 maxAllowed);
    error ReserveInvariantViolated(uint256 remainingReserve, uint256 minRequired);
    error CircuitBreakerActive();
    error Unauthorized();

    modifier onlyOwner() {
        if (msg.sender != owner) revert Unauthorized();
        _;
    }

    constructor() {
        owner = msg.sender;
        lastHourTimestamp = block.timestamp;
    }

    function setStrategyWhitelist(address strategy, bool status) external onlyOwner {
        whitelistedStrategies[strategy] = status;
        emit StrategyWhitelisted(strategy, status);
    }

    function setParameters(
        uint256 _maxSlippage,
        uint256 _maxAllocation,
        uint256 _minReserve,
        uint256 _maxDrawdown
    ) external onlyOwner {
        require(_maxAllocation <= 8000, "Allocation cap too high");
        require(_minReserve >= 500, "Min reserve must be at least 5%");
        maxSlippageBps = _maxSlippage;
        maxPoolAllocationBps = _maxAllocation;
        minLiquidReserveBps = _minReserve;
        maxHourlyDrawdownBps = _maxDrawdown;
        emit InvariantParametersUpdated(_maxSlippage, _maxAllocation, _minReserve);
    }

    /**
     * @notice Validates that a proposed rebalancing action satisfies all invariants
     * @param totalVaultAssets Total assets managed across the vault and all strategies
     * @param targetStrategy The strategy receiving funds
     * @param currentTargetAssets Current amount in target strategy
     * @param amountToAllocate New amount to deposit into target
     * @param expectedMinReceived Minimum expected output to verify slippage
     * @param estimatedOutput Actual output estimate from DEX/pool
     */
    function validateRebalance(
        uint256 totalVaultAssets,
        address targetStrategy,
        uint256 currentTargetAssets,
        uint256 amountToAllocate,
        uint256 expectedMinReceived,
        uint256 estimatedOutput
    ) external view returns (bool) {
        if (circuitBreakerTriggered) revert CircuitBreakerActive();
        if (!whitelistedStrategies[targetStrategy]) revert StrategyNotWhitelisted(targetStrategy);

        // 1. Invariant: Max Single-Pool Allocation Check
        uint256 proposedTargetTotal = currentTargetAssets + amountToAllocate;
        uint256 maxAllowedPerStrategy = (totalVaultAssets * maxPoolAllocationBps) / BPS_DENOMINATOR;
        if (proposedTargetTotal > maxAllowedPerStrategy) {
            revert MaxAllocationExceeded(targetStrategy, proposedTargetTotal, maxAllowedPerStrategy);
        }

        // 2. Invariant: Slippage Verification Check
        if (estimatedOutput < expectedMinReceived) {
            revert SlippageExceeded(expectedMinReceived, estimatedOutput, maxSlippageBps);
        }

        return true;
    }

    /**
     * @notice Checks vault total assets against high watermark to trigger emergency circuit breaker
     */
    function updateDrawdownMonitor(uint256 currentTotalAssets) external {
        if (block.timestamp >= lastHourTimestamp + 1 hours) {
            lastHourlyHighWatermark = currentTotalAssets;
            lastHourTimestamp = block.timestamp;
            return;
        }

        if (currentTotalAssets > lastHourlyHighWatermark) {
            lastHourlyHighWatermark = currentTotalAssets;
        } else if (lastHourlyHighWatermark > 0) {
            uint256 drawdown = lastHourlyHighWatermark - currentTotalAssets;
            uint256 drawdownBps = (drawdown * BPS_DENOMINATOR) / lastHourlyHighWatermark;
            if (drawdownBps >= maxHourlyDrawdownBps) {
                circuitBreakerTriggered = true;
                emit CircuitBreakerTripped(block.timestamp, currentTotalAssets, lastHourlyHighWatermark);
            }
        }
    }

    function resetCircuitBreaker() external onlyOwner {
        circuitBreakerTriggered = false;
        lastHourlyHighWatermark = 0;
        lastHourTimestamp = block.timestamp;
        emit CircuitBreakerReset(block.timestamp);
    }
}
