// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./interfaces/IERC20.sol";
import "./interfaces/ISett.sol";
import "./interfaces/IGeyser.sol";
import "./interfaces/IUniswapV2Pair.sol";
import "./interfaces/ICToken.sol";
import "./interfaces/IBridgePool.sol";

contract ArbBadgerVotingShare {
    IERC20 constant badger = IERC20(0xBfa641051Ba0a0Ad1b0AcF549a89536A0D76472E);

    //Badger is token1
    IUniswapV2Pair constant badger_weth_swapr =
        IUniswapV2Pair(0x3C6bd88cdD2AECf466E22d4ED86dB6B8953FDb72);
    ISett constant sett_badger_weth_swapr =
        ISett(0xE9C12F06F8AFFD8719263FE4a81671453220389c);


    function decimals() external pure returns (uint8) {
        return uint8(18);
    }

    function name() external pure returns (string memory) {
        return "Badger Voting Share";
    }

    function symbol() external pure returns (string memory) {
        return "Badger VS";
    }

    function totalSupply() external view returns (uint256) {
        return badger.totalSupply();
    }

    function swaprBalanceOf(address _voter) external view returns(uint256) {
        return _swaprBalanceOf(_voter);
    }
    function badgerBalanceOf(address _voter) external view returns(uint256) {
        return badger.balanceOf(_voter);
    }

    
    function _swaprBalanceOf(address _voter) internal view returns (uint256) {
        /// @notice Calculate the badger balance of a voter from their swapr LP
        /// @dev There are 2 different ways to have this, just plain LP and LP deposited in a vault
        /// @param _voter address of the voter
        /// @return amount of badger held in LP in wei format
        uint256 bSwaprPricePerShare = sett_badger_weth_swapr
            .getPricePerFullShare();
        (, uint112 reserve1, ) = badger_weth_swapr.getReserves();
        uint256 totalSwaprBalance = badger_weth_swapr.balanceOf(_voter) +
            (sett_badger_weth_swapr.balanceOf(_voter) * bSwaprPricePerShare) /
            1e18;
        return (totalSwaprBalance * reserve1) / badger_weth_swapr.totalSupply();
    }


    function balanceOf(address _voter) external view returns (uint256) {
        /// @notice Calculate the total aggregate balance of a voter in badger
        /// @dev Includes all accepted voting forms of holdings for a user
        /// @param _voter address of the voter
        /// @return total aggregate amount of badger in wei format
        return
            badger.balanceOf(_voter) +
            _swaprBalanceOf(_voter);
    }

    constructor() {}
}
