// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ICToken {
    function balanceOf(address owner) external view returns (uint256);
    function exchangeRateCurrent() external view returns (uint);
}
