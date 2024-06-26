// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./interfaces/IERC20.sol";
import "./interfaces/ISett.sol";
import "./interfaces/IGeyser.sol";
import "./interfaces/IUniswapV2Pair.sol";
import "./interfaces/ICToken.sol";
import "./interfaces/IBridgePool.sol";
import "./interfaces/ICurvePool.sol";
import "./interfaces/ICurveToken.sol";
import "./interfaces/IVault.sol";
import "./interfaces/IBalancerPoolToken.sol";
import "./interfaces/IBremBadger.sol";

contract BadgerVotingShare {
    IERC20 constant badger = IERC20(0x3472A5A71965499acd81997a54BBA8D852C6E53d);
    ISett constant sett_badger =
        ISett(0x19D97D8fA813EE2f51aD4B4e04EA08bAf4DFfC28);
    IGeyser constant geyser_badger =
        IGeyser(0xa9429271a28F8543eFFfa136994c0839E7d7bF77);
    ISett constant rem_badger =
        ISett(0x6aF7377b5009d7d154F36FE9e235aE1DA27Aea22);
    IBremBadger constant bremBadger =
        IBremBadger(0x170D9fA0Cb0226f0d87952905228e5AA7323DdA6);

    //Badger is token1
    IUniswapV2Pair constant badger_wBTC_UniV2 =
        IUniswapV2Pair(0xcD7989894bc033581532D2cd88Da5db0A4b12859);
    ISett constant sett_badger_wBTC_UniV2 =
        ISett(0x235c9e24D3FB2FAFd58a2E49D454Fdcd2DBf7FF1);
    IGeyser constant geyser_badger_wBTC_UniV2 =
        IGeyser(0xA207D69Ea6Fb967E54baA8639c408c31767Ba62D);

    //Badger is token1
    IUniswapV2Pair constant badger_wBTC_SLP =
        IUniswapV2Pair(0x110492b31c59716AC47337E616804E3E3AdC0b4a);
    ISett constant sett_badger_wBTC_SLP =
        ISett(0x1862A18181346EBd9EdAf800804f89190DeF24a5);
    IGeyser constant geyser_badger_wBTC_SLP =
        IGeyser(0xB5b654efBA23596Ed49FAdE44F7e67E23D6712e7);

    IBridgePool constant aBADGER =
        IBridgePool(0x43298F9f91a4545dF64748e78a2c777c580573d6);

    ICurvePool constant badger_wBTC_crv_pool =
        ICurvePool(0x50f3752289e1456BfA505afd37B241bca23e685d);
    ICurveToken constant badger_wBTC_crv_token =
        ICurveToken(0x137469B55D1f15651BA46A89D0588e97dD0B6562);
    ISett constant sett_badger_wBTC_crv =
        ISett(0xeC1c717A3b02582A4Aa2275260C583095536b613);

    // Balancer Vault
    IVault constant balancer_vault =
        IVault(0xBA12222222228d8Ba445958a75a0704d566BF2C8);

    IBalancerPoolToken constant badger_wBTC_balancer =
        IBalancerPoolToken(0xb460DAa847c45f1C4a41cb05BFB3b51c92e41B36);
    ISett constant sett_badger_wBTC_balancer =
        ISett(0x63ad745506BD6a3E57F764409A47ed004BEc40b1);
    IERC20 constant bptStakedBadgerWbtc =
        IERC20(0x3F29e69955E5202759208DD0C5E0BA55ff934814);
    IERC20 constant bptAuraBadgerWbtc =
        IERC20(0xddf14A569dD91AF895E3B05d6dBCBB9db1c3834C);

    IBalancerPoolToken constant badgerRethBalancer =
        IBalancerPoolToken(0x1ee442b5326009Bb18F2F472d3e0061513d1A0fF);
    IERC20 constant bptStakedBadgerReth =
        IERC20(0x87012b0C3257423fD74a5986F81a0f1954C17a1d);
    IERC20 constant bptAuraBadgerReth =
        IERC20(0xAAd4eE162Dbc9C25cCa26bA4340B36E3eF7C1A80);

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

    function uniswapBalanceOf(address _voter) external view returns (uint256) {
        return _uniswapBalanceOf(_voter);
    }

    function sushiswapBalanceOf(
        address _voter
    ) external view returns (uint256) {
        return _sushiswapBalanceOf(_voter);
    }

    function badgerBalanceOf(address _voter) external view returns (uint256) {
        return _badgerBalanceOf(_voter);
    }

    function remBadgerBalanceOf(
        address _voter
    ) external view returns (uint256) {
        return _remBadgerBalanceOf(_voter);
    }

    function bremBadgerBalanceOf(
        address _voter
    ) external view returns (uint256) {
        return _bremBadgerBalanceOf(_voter);
    }

    function acrossBalanceOf(address _voter) external view returns (uint256) {
        return _acrossBalanceOf(_voter);
    }

    function curveBalanceOf(address _voter) external view returns (uint256) {
        return _curveBalanceOf(_voter);
    }

    function balancerBadgerWbtcBalanceOf(
        address _voter
    ) external view returns (uint256) {
        return _balancerBadgerWbtcBalanceOf(_voter);
    }

    function balancerBadgerRethBalanceOf(
        address _voter
    ) external view returns (uint256) {
        return _balancerBadgerRethBalanceOf(_voter);
    }

    /*
        The voter can have Badger in Uniswap in 3 configurations:
         * Staked bUni-V2 in Geyser
         * Unstaked bUni-V2 (same as staked Uni-V2 in Sett)
         * Unstaked Uni-V2
        The top two correspond to more than 1 Uni-V2, so they are multiplied by pricePerFullShare.
        After adding all 3 balances we calculate how much BADGER it corresponds to using the pool's reserves.
    */
    function _uniswapBalanceOf(address _voter) internal view returns (uint256) {
        uint256 bUniV2PricePerShare = sett_badger_wBTC_UniV2
            .getPricePerFullShare();
        (, uint112 reserve1, ) = badger_wBTC_UniV2.getReserves();
        uint256 totalUniBalance = badger_wBTC_UniV2.balanceOf(_voter) +
            (sett_badger_wBTC_UniV2.balanceOf(_voter) * bUniV2PricePerShare) /
            1e18 +
            (geyser_badger_wBTC_UniV2.totalStakedFor(_voter) *
                bUniV2PricePerShare) /
            1e18;
        return (totalUniBalance * reserve1) / badger_wBTC_UniV2.totalSupply();
    }

    /*
        The voter can have Badger in Sushi in 3 configurations:
         * Staked SLP in Geyser
         * Unstaked SLP (same as staked SLP in Sett)
         * Unstaked SLP
        The top two correspond to more than 1 SLP, so they are multiplied by pricePerFullShare.
        After adding all 3 balances we calculate how much BADGER it corresponds to using the pool's reserves.
    */
    function _sushiswapBalanceOf(
        address _voter
    ) internal view returns (uint256) {
        uint256 total = badger_wBTC_SLP.totalSupply();
        if (total == 0) {
            return 0;
        }
        uint256 bSLPPricePerShare = sett_badger_wBTC_SLP.getPricePerFullShare();
        (, uint112 reserve1, ) = badger_wBTC_SLP.getReserves();
        uint256 totalSLPBalance = badger_wBTC_SLP.balanceOf(_voter) +
            (sett_badger_wBTC_SLP.balanceOf(_voter) * bSLPPricePerShare) /
            1e18 +
            (geyser_badger_wBTC_SLP.totalStakedFor(_voter) *
                bSLPPricePerShare) /
            1e18;
        return (totalSLPBalance * reserve1) / total;
    }

    /*
        The voter can have Badger in Curve in 2 configurations:
         * Curve LP in vault
         * Curve LP in wallet
        Vaults have an additional PPFS that we need to take into account
        After adding the 2 balances we calculate how much BADGER it corresponds to using the pool's reserves.
    */
    function _curveBalanceOf(address _voter) internal view returns (uint256) {
        uint256 total = badger_wBTC_crv_token.totalSupply();
        if (total == 0) {
            return 0;
        }
        // coin 0 is BADGER
        uint256 bCrvPricePerShare = sett_badger_wBTC_crv.getPricePerFullShare();
        uint256 poolBadgerBalance = badger_wBTC_crv_pool.balances(0);
        uint256 voterLpBalance = badger_wBTC_crv_token.balanceOf(_voter) +
            (sett_badger_wBTC_crv.balanceOf(_voter) * bCrvPricePerShare) /
            1e18;
        return (voterLpBalance * poolBadgerBalance) / total;
    }

    /*
        The voter can have regular Badger in 3 configurations as well:
         * Staked bBadger in Geyser
         * Unstaked bBadger (same as staked Badger in Sett)
         * Unstaked Badger
    */
    function _badgerBalanceOf(address _voter) internal view returns (uint256) {
        uint256 bBadgerPricePerShare = sett_badger.getPricePerFullShare();
        return
            badger.balanceOf(_voter) +
            (sett_badger.balanceOf(_voter) * bBadgerPricePerShare) /
            1e18 +
            (geyser_badger.totalStakedFor(_voter) * bBadgerPricePerShare) /
            1e18;
    }

    /*
        The voter can also have remBADGER
    */
    function _remBadgerBalanceOf(
        address _voter
    ) internal view returns (uint256) {
        uint256 remBadgerPricePerShare = rem_badger.getPricePerFullShare();
        return (rem_badger.balanceOf(_voter) * remBadgerPricePerShare) / 1e18;
    }

    /*
        The voter can also have bremBADGER
    */
    function _bremBadgerBalanceOf(
        address _voter
    ) internal view returns (uint256) {
        uint256 remBadgerBalance = bremBadger.totalDeposited(_voter) -
            bremBadger.totalClaimed(_voter);
        return (remBadgerBalance * rem_badger.getPricePerFullShare()) / 1e18;
    }

    /*
        The voter may have deposited BADGER into the across pool:
    */
    function _acrossBalanceOf(address _voter) internal view returns (uint256) {
        uint256 total = aBADGER.totalSupply();
        if (total == 0) {
            return 0;
        }
        int256 numerator = int256(aBADGER.liquidReserves()) +
            int256(aBADGER.utilizedReserves()) -
            int256(aBADGER.undistributedLpFees());
        uint256 exchangeRateCurrent = (uint256(numerator) * 1e18) / total;

        return (exchangeRateCurrent * aBADGER.balanceOf(_voter)) / 1e18;
    }

    /*
        The voter can have BadgerWbtc in Balancer in 4 configurations:
         * Balancer BPT in wallet
         * Balancer BPT in sett
         * Balancer BPT in balancer gauge
         * Balancer BPT in aura gauge
        Setts have an additional PPFS that we need to take into account
    */
    function _balancerBadgerWbtcBalanceOf(
        address _voter
    ) internal view returns (uint256) {
        bytes32 poolId = badger_wBTC_balancer.getPoolId();
        (IERC20[] memory tokens, uint256[] memory balances, ) = balancer_vault
            .getPoolTokens(poolId);
        uint256 poolBadgerAmount;
        for (uint256 i = 0; i < tokens.length; i++) {
            if (tokens[i] == badger) {
                poolBadgerAmount = balances[i];
                break;
            }
        }

        uint256 bptTotalSupply = badger_wBTC_balancer.totalSupply();
        if (bptTotalSupply == 0) {
            return 0;
        }
        uint256 voterBalance = badger_wBTC_balancer.balanceOf(_voter);
        uint256 voterVaultBalance = sett_badger_wBTC_balancer.balanceOf(_voter);
        uint256 voterStakedBalance = bptStakedBadgerWbtc.balanceOf(_voter);
        uint256 voterAuraBalance = bptAuraBadgerWbtc.balanceOf(_voter);
        uint256 vaultPPFS = sett_badger_wBTC_balancer.getPricePerFullShare();

        uint256 bptVotes = (voterBalance * poolBadgerAmount) / bptTotalSupply;
        uint256 bptStakedVotes = (voterStakedBalance * poolBadgerAmount) /
            bptTotalSupply;
        uint256 bptAuraVotes = (voterAuraBalance * poolBadgerAmount) /
            bptTotalSupply;
        uint256 bptSettVotes = (voterVaultBalance *
            poolBadgerAmount *
            vaultPPFS) /
            bptTotalSupply /
            1e18;
        return bptVotes + bptStakedVotes + bptAuraVotes + bptSettVotes;
    }

    /*
        The voter can have BadgerReth in Balancer in 3 configurations:
         * Balancer BPT in wallet
         * Balancer BPT in balancer gauge
         * Balancer BPT in aura gauge
        Setts have an additional PPFS that we need to take into account
    */
    function _balancerBadgerRethBalanceOf(
        address _voter
    ) internal view returns (uint256) {
        bytes32 poolId = badgerRethBalancer.getPoolId();
        (IERC20[] memory tokens, uint256[] memory balances, ) = balancer_vault
            .getPoolTokens(poolId);
        uint256 poolBadgerAmount;
        for (uint i = 0; i < tokens.length; i++) {
            if (tokens[i] == badger) {
                poolBadgerAmount = balances[i];
                break;
            }
        }

        uint256 bptTotalSupply = badgerRethBalancer.totalSupply();
        if (bptTotalSupply == 0) {
            return 0;
        }
        uint256 voterBalance = badgerRethBalancer.balanceOf(_voter);

        uint256 bptVotes = (voterBalance * poolBadgerAmount) / bptTotalSupply;
        uint256 bptStakedVotes = (bptStakedBadgerReth.balanceOf(_voter) *
            poolBadgerAmount) / bptTotalSupply;
        uint256 bptAuraVotes = (bptAuraBadgerReth.balanceOf(_voter) *
            poolBadgerAmount) / bptTotalSupply;
        return bptVotes + bptStakedVotes + bptAuraVotes;
    }

    function balanceOf(address _voter) external view returns (uint256) {
        return
            _badgerBalanceOf(_voter) +
            _uniswapBalanceOf(_voter) +
            _sushiswapBalanceOf(_voter) +
            _remBadgerBalanceOf(_voter) +
            _bremBadgerBalanceOf(_voter) +
            _acrossBalanceOf(_voter) +
            _curveBalanceOf(_voter) +
            _balancerBadgerWbtcBalanceOf(_voter) +
            _balancerBadgerRethBalanceOf(_voter);
    }

    constructor() {}
}
