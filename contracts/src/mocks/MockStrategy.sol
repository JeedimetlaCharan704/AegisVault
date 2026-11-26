// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../interfaces/IStrategy.sol";

contract MockERC20 {
    string public name = "USD Coin Mock";
    string public symbol = "USDC";
    uint8 public constant decimals = 6;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
        totalSupply += amount;
        emit Transfer(address(0), to, amount);
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        require(balanceOf[msg.sender] >= amount, "ERC20: transfer amount exceeds balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        require(balanceOf[from] >= amount, "ERC20: balance low");
        if (allowance[from][msg.sender] != type(uint256).max) {
            require(allowance[from][msg.sender] >= amount, "ERC20: allowance low");
            allowance[from][msg.sender] -= amount;
        }
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
        return true;
    }
}

contract MockStrategy is IStrategy {
    address public immutable override asset;
    string public strategyName;
    uint256 public simulatedAPY; // in BPS (e.g. 850 = 8.5%)
    uint256 public simulatedHealthScore = 98; // 0 - 100
    bool public isPaused;

    uint256 private _totalAssets;

    event AnomalyTriggered(string strategyName, uint256 newHealthScore);

    constructor(address _asset, string memory _name, uint256 _apy) {
        asset = _asset;
        strategyName = _name;
        simulatedAPY = _apy;
    }

    function totalAssets() external view override returns (uint256) {
        return _totalAssets;
    }

    function currentAPY() external view override returns (uint256) {
        return simulatedAPY;
    }

    function healthScore() external view override returns (uint256) {
        return simulatedHealthScore;
    }

    function isEmergencyPaused() external view override returns (bool) {
        return isPaused;
    }

    function deposit(uint256 amount) external override returns (uint256) {
        require(!isPaused, "Strategy paused");
        MockERC20(asset).transferFrom(msg.sender, address(this), amount);
        _totalAssets += amount;
        return amount;
    }

    function withdraw(uint256 amount, address recipient) external override returns (uint256) {
        uint256 actualAmount = amount > _totalAssets ? _totalAssets : amount;
        _totalAssets -= actualAmount;
        MockERC20(asset).transfer(recipient, actualAmount);
        return actualAmount;
    }

    // --- Interactive Simulation Functions for Testing ---
    function setAPY(uint256 _apy) external {
        simulatedAPY = _apy;
    }

    function triggerAnomaly(uint256 newHealthScore) external {
        simulatedHealthScore = newHealthScore;
        emit AnomalyTriggered(strategyName, newHealthScore);
    }
}
