// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IStrategy
 * @notice Standard interface for external DeFi yield strategies integrated into AegisVault
 */
interface IStrategy {
    function asset() external view returns (address);
    function totalAssets() external view returns (uint256);
    function deposit(uint256 amount) external returns (uint256 shares);
    function withdraw(uint256 amount, address recipient) external returns (uint256 actualAmount);
    function currentAPY() external view returns (uint256 bps);
    function healthScore() external view returns (uint256 score); // 0 - 100
    function isEmergencyPaused() external view returns (bool);
}
