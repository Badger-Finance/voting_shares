from decimal import Decimal
from shutil import ExecError
from brownie import Wei
from datetime import datetime, timedelta
import pytest
from brownie.network.gas.strategies import ExponentialScalingStrategy


########### GENERAL FIXTURES ###########

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def wbtc_whale(accounts):
    return accounts.at("0xC564EE9f21Ed8A2d8E7e76c085740d5e4c5FaFbE", force=True)

@pytest.mark.require_network("arb-main-fork")
@pytest.fixture(scope="module")
def arb_weth_whale(accounts):
    return accounts.at("0x80A9ae39310abf666A87C743d6ebBD0E8C42158E", force=True)

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def wBTC(interface):
    return interface.IERC20("0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599")

@pytest.mark.require_network("arb-main-fork")
@pytest.fixture(scope="module")
def arb_weth(interface):
    return interface.IERC20("0x82aF49447D8a07e3bd95BD0d56f35241523fBab1")


########### DIGG FIXTURES ###########

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def random_digg_depositor(accounts):
    return accounts.at("0xF8dbb94608E72A3C4cEeAB4ad495ac51210a341e", force=True)

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def digg_whale(accounts):
    return accounts.at("0xfed1CAe770ca1cD19D7bcC7Fa61d3325A9d5D164", force=True)

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def fDigg(interface):
    return interface.ICToken("0x792a676dD661E2c182435aaEfC806F1d4abdC486")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def digg(interface):
    return interface.IERC20("0x798d1be841a82a273720ce31c822c61a67a601c3")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def digg_wBTC_UniV2(interface):
    return interface.IUniswapV2Pair("0xE86204c4eDDd2f70eE00EAd6805f917671F56c52")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def digg_wBTC_SLP(interface):
    return interface.IUniswapV2Pair("0x9a13867048e01c663ce8Ce2fE0cDAE69Ff9F35E3")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def sushi_router(interface):
    return interface.IUniswapV2Router01("0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def uni_router(interface):
    return interface.IUniswapV2Router01("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")

@pytest.mark.require_network("arb-main-fork")
@pytest.fixture(scope="module")
def swapr_router(interface):
    return interface.IUniswapV2Router01("0x530476d5583724A89c8841eB6Da76E7Af4C0F17E")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def digg_sett(interface):
    return interface.ISett("0x7e7E112A68d8D2E221E11047a72fFC1065c38e1a")


########### BADGER FIXTURES ###########

@pytest.fixture(scope="module")
def random_minter(accounts):
    yield accounts.at("0xF8dbb94608E72A3C4cEeAB4ad495ac51210a341e", force=True)

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def badger_whale(accounts):
    yield accounts.at("0x34e2741a3F8483dBe5231F61C005110ff4B9F50A", force=True)

@pytest.mark.require_network("arb-main-fork")
@pytest.fixture(scope="module")
def arb_badger_whale(accounts):
    yield accounts.at("0x3bd856465321ead1605286938493169E9C9011Cf", force=True)

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def fBadger(interface):
    yield interface.ICToken("0x6780B4681aa8efE530d075897B3a4ff6cA5ed807")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def badger_wBTC_univ2(interface):
    return interface.IUniswapV2Pair("0xcd7989894bc033581532d2cd88da5db0a4b12859")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def badger_wBTC_SLP(interface):
    return interface.IUniswapV2Pair("0x110492b31c59716ac47337e616804e3e3adc0b4a")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def badger_sett(interface):
    return interface.ISett("0x19D97D8fA813EE2f51aD4B4e04EA08bAf4DFfC28")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def badger(interface):
    yield interface.IERC20("0x3472A5A71965499acd81997a54BBA8D852C6E53d")

@pytest.mark.require_network("arb-main-fork")
@pytest.fixture(scope="module")
def arb_badger(interface):
    yield interface.IERC20("0xBfa641051Ba0a0Ad1b0AcF549a89536A0D76472E")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def remBadger(interface):
    yield interface.ISett("0x6aF7377b5009d7d154F36FE9e235aE1DA27Aea22")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def aBadger(interface):
    yield interface.IBridgePool("0x43298F9f91a4545dF64748e78a2c777c580573d6")

@pytest.mark.require_network("arb-main-fork")
@pytest.fixture(scope="module")
def badger_wETH_swapr(interface):
    yield interface.IUniswapV2Pair("0x3C6bd88cdD2AECf466E22d4ED86dB6B8953FDb72")

@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def badger_wBTC_crv_pool(interface):
    yield interface.ICurvePool("0x50f3752289e1456BfA505afd37B241bca23e685d")


@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def badger_wBTC_crv_token(interface):
    yield interface.ICurveToken("0x137469B55D1f15651BA46A89D0588e97dD0B6562")


@pytest.mark.require_network("mainnet-fork")
@pytest.fixture(scope="module")
def badger_wBTC_crv_vault(interface):
    yield interface.ISett("0x6aF7377b5009d7d154F36FE9e235aE1DA27Aea22")


########### HELPER FUNCTIONS ###########

def univ2_deposit(lp_pair, token0, token0_decimals, token1, token1_decimals, token1_amount, router, depositor, whale):
    test_amount_token1 = Wei(token1_amount * token1_decimals)
    # 5% slippage for depositing
    slippage = 0.95

    # get current reserves to see deposit ratio
    (reserve0, reserve1, _) = lp_pair.getReserves()
    reserve0_normalized = reserve0 / token0_decimals
    reserve1_normalized = reserve1 / token1_decimals

    # We want to know how much token0 to deposit to maintain token1 levels
    test_amount_token0 = int((test_amount_token1 / token1_decimals) * (reserve0_normalized / reserve1_normalized) * token0_decimals)

    print(f"Depositing {test_amount_token0} token0 and {test_amount_token1} token1")

    now = datetime.now()
    deadline = now + timedelta(minutes=30)
    deadline_unix = deadline.timestamp()
    min_token1 = int(test_amount_token1 * slippage)
    min_token0 = int(test_amount_token0 * slippage)

    #  transfer token1 to deposit
    token1.transfer(depositor, test_amount_token1, {"from": whale[token1], "gas_price": ExponentialScalingStrategy(7, 200)})
    print(f"Transferred: {test_amount_token1} token1 {token1.balanceOf(depositor)}")
    # transfer token0 to deposit
    token0.transfer(depositor, test_amount_token0, {"from": whale[token0], "gas_price": ExponentialScalingStrategy(7, 200)})
    print(f"Transferred: {test_amount_token0} token0 {token0.balanceOf(depositor)}")

    # approve token1 for deposit
    token1.approve(router, test_amount_token1, {"from": depositor, "gas_price": ExponentialScalingStrategy(7, 200)})
    # approve token0 for deposit
    token0.approve(router, test_amount_token0, {"from": depositor, "gas_price": ExponentialScalingStrategy(7, 200)})
    # deposit
    router.addLiquidity(token0, token1, test_amount_token0, test_amount_token1, min_token0, min_token1, depositor, deadline_unix, {"from": depositor, "gas_price": ExponentialScalingStrategy(7, 200)})


########### DIGG TEST SETUP ###########

@pytest.fixture(scope="module")
def prep_mint_bDigg(digg_whale, random_digg_depositor, digg, digg_sett):
    test_amount = 1*1e9
    print(f"Transferring: {test_amount} = {test_amount / 1e9} DIGG")
    #  transfer 1 DIGG to minter
    digg.transfer(random_digg_depositor, test_amount, {"from": digg_whale, "gas_price": ExponentialScalingStrategy(7, 200)})
    print(f"Transferred: {test_amount} DIGG {digg.balanceOf(random_digg_depositor)}")

    # approve DIGG for deposit into vault
    digg.approve(digg_sett, test_amount, {"from": random_digg_depositor, "gas_price": ExponentialScalingStrategy(7, 200)})
    # deposit into vault
    digg_sett.deposit(test_amount, {"from": random_digg_depositor, "gas_price": ExponentialScalingStrategy(7, 200)})

    digg_sett_balance = digg_sett.balanceOf(random_digg_depositor)
    print(f"bDIGG received: {digg_sett_balance}")
    digg_ppfs = digg_sett.balance() / digg_sett.totalSupply()
    print(f"Converts to: {digg_sett_balance * digg_ppfs / 1e9} deposited digg")

@pytest.fixture(scope="module")
def prep_mint_fDigg(digg_whale, random_digg_depositor, digg, fDigg):
    test_amount = 1*1e9
    print(f"Transferring: {test_amount} = {test_amount / 1e9} DIGG")
    #  transfer 1 DIGG to minter
    digg.transfer(random_digg_depositor, test_amount, {"from": digg_whale, "gas_price": ExponentialScalingStrategy(7, 200)})
    print(f"Transferred: {test_amount} DIGG {digg.balanceOf(random_digg_depositor)}")

    # approve DIGG for minting
    digg.approve(fDigg, test_amount, {"from": random_digg_depositor, "gas_price": ExponentialScalingStrategy(7, 200)})
    # mint
    fDigg.mint(test_amount, {"from": random_digg_depositor, "gas_price": ExponentialScalingStrategy(7, 200)})
    # print Exchange Rate
    print(f"Exchange rate: {fDigg.exchangeRateStored()}")
    print(f"Amount Minted: {fDigg.balanceOf(random_digg_depositor)}")
    print(f"Digg balance: {digg.balanceOf(random_digg_depositor)}")

@pytest.fixture(scope="module")
def prep_mint_sushi(digg_whale, wbtc_whale, random_digg_depositor, digg, wBTC, digg_wBTC_SLP, sushi_router):
    univ2_deposit(digg_wBTC_SLP, wBTC, 1e8, digg, 1e9, 1, sushi_router, random_digg_depositor, {digg: digg_whale, wBTC: wbtc_whale})
    print(f"Deposited to sushi, got {digg_wBTC_SLP.balanceOf(random_digg_depositor)} SLP")

@pytest.fixture(scope="module")
def prep_mint_uni(digg_whale, wbtc_whale, random_digg_depositor, digg, wBTC, digg_wBTC_UniV2, uni_router):
    univ2_deposit(digg_wBTC_UniV2, wBTC, 1e8, digg, 1e9, 1, uni_router, random_digg_depositor, {digg: digg_whale, wBTC: wbtc_whale})
    print(f"Deposited to uni, got {digg_wBTC_UniV2.balanceOf(random_digg_depositor)} UniV2")

@pytest.fixture(scope="module")
def digg_voter(DiggVotingShare, random_digg_depositor):
    diggVotingShare = DiggVotingShare.deploy({"from": random_digg_depositor, "gas_price": ExponentialScalingStrategy(7, 200)})
    return diggVotingShare


########### BADGER TEST SETUP ###########

@pytest.fixture(scope="module")
def prep_mint_bBadger(badger_whale, random_minter, badger, badger_sett):
    test_amount = 1 * 1e18
    print(f"Transferring: {test_amount} = {test_amount / 1e18} BADGER")
    #  transfer 1 BADGER to minter
    badger.transfer(random_minter, test_amount, {"from": badger_whale, "gas_price": ExponentialScalingStrategy(7, 200)})
    print(f"Transferred: {test_amount} BADGER = {badger.balanceOf(random_minter)}")

    # approve BADGER for deposit into vault
    badger.approve(badger_sett, test_amount, {"from": random_minter, "gas_price": ExponentialScalingStrategy(7, 200)})
    # deposit into vault
    badger_sett.deposit(test_amount, {"from": random_minter, "gas_price": ExponentialScalingStrategy(7, 200)})

    badger_sett_balance = badger_sett.balanceOf(random_minter)
    print(f"bBadger received: {badger_sett_balance}")
    badger_ppfs = badger_sett.balance() / badger_sett.totalSupply()
    print(f"Converts to: {badger_sett_balance * badger_ppfs / 1e18} deposited badger")

@pytest.fixture(scope="module")
def prep_mint_arb_badger(arb_badger_whale, random_minter, arb_badger):
    test_amount = 1 * 1e18
    print(f"Transferring: {test_amount} = {test_amount / 1e18} BADGER")
    #  transfer 1 BADGER to minter
    arb_badger.transfer(random_minter, test_amount, {"from": arb_badger_whale, "gas_price": ExponentialScalingStrategy(7, 200)})
    print(f"Transferred: {test_amount} BADGER = {arb_badger.balanceOf(random_minter)}")

@pytest.fixture(scope="module")
def prep_mint_fBadger(badger_whale, random_minter, badger, fBadger):
    test_amount = 1e19
    print(f"test amount: {test_amount}")
    print(f"badger before: {badger.balanceOf(random_minter)}")
    #  transfer from whale to 1 BADGER
    badger.transfer(random_minter, test_amount, {"from": badger_whale, "gas_price": ExponentialScalingStrategy(7, 200)})
    # approve BADGER for minting
    print(f"badger after: {badger.balanceOf(random_minter)}")
    badger.approve(fBadger, test_amount, {"from": random_minter, "gas_price": ExponentialScalingStrategy(7, 200)})
    # mint
    mint_sim = fBadger.mint.call(test_amount, {"from": random_minter})
    print(f"mint sim: {mint_sim}")
    try:
        mint_return = fBadger.mint(test_amount / 2, {"from": random_minter})
    except Exception as e:
        print("error:", e)
    print(f"mint return: {mint_return.return_value}")
    print(f"fBadger minting: {fBadger.balanceOf(random_minter)}")

@pytest.fixture(scope="module")
def badger_voter(BadgerVotingShare, random_minter):
    badgerVotingShare = BadgerVotingShare.deploy({"from": random_minter, "gas_price": ExponentialScalingStrategy(7, 200)})
    yield badgerVotingShare

@pytest.fixture(scope="module")
def arb_badger_voter(ArbBadgerVotingShare, random_minter):
    badgerVotingShare = ArbBadgerVotingShare.deploy({"from": random_minter, "gas_price": ExponentialScalingStrategy(7, 200)})
    yield badgerVotingShare

@pytest.fixture(scope="module")
def prep_mint_badger_uni(badger_whale, wbtc_whale, random_minter, badger, wBTC, badger_wBTC_univ2, uni_router):
    univ2_deposit(badger_wBTC_univ2, wBTC, 1e8, badger, 1e18, 1, uni_router, random_minter, {badger: badger_whale, wBTC: wbtc_whale})
    print(f"Deposited to uni, got {badger_wBTC_univ2.balanceOf(random_minter)} UniV2")

@pytest.fixture(scope="module")
def prep_mint_arb_swapr(arb_badger_whale, arb_weth_whale, random_minter, arb_badger, arb_weth, badger_wETH_swapr, swapr_router):
    univ2_deposit(badger_wETH_swapr, arb_weth, 1e18, arb_badger, 1e18, 1, swapr_router, random_minter, {arb_badger: arb_badger_whale, arb_weth: arb_weth_whale})
    print(f"Deposited to swapr, got {badger_wETH_swapr.balanceOf(random_minter)} UniV2")

@pytest.fixture(scope="module")
def prep_mint_badger_sushi(badger_whale, wbtc_whale, random_minter, badger, wBTC, badger_wBTC_SLP, sushi_router):
    univ2_deposit(badger_wBTC_SLP, wBTC, 1e8, badger, 1e18, 1, sushi_router, random_minter, {badger: badger_whale, wBTC: wbtc_whale})
    print(f"Deposited to sushi, got {badger_wBTC_SLP.balanceOf(random_minter)} SLP")

@pytest.fixture(scope="module")
def prep_mint_abadger(badger_whale, random_minter, badger, aBadger):
    test_amount = 1 * 1e18
    print(f"Transferring: {test_amount} = {test_amount / 1e18} BADGER")
    #  transfer 1 BADGER to minter
    badger.transfer(random_minter, test_amount, {"from": badger_whale, "gas_price": ExponentialScalingStrategy(7, 200)})
    print(f"Transferred: {test_amount} BADGER = {badger.balanceOf(random_minter)}")
    # approve BADGER for deposit into vault
    badger.approve(aBadger, test_amount, {"from": random_minter, "gas_price": ExponentialScalingStrategy(7, 200)})
    aBadger.addLiquidity(test_amount, {"from": random_minter, "gas_price": ExponentialScalingStrategy(7, 200)})

    print(f'Minted {aBadger.balanceOf(random_minter)} aBADGER')

@pytest.fixture(scope="module")
def prep_mint_curve(badger_whale, wbtc_whale, random_minter, badger, wBTC, badger_wBTC_crv_pool, badger_wBTC_crv_token):
    test_amount_badger = Decimal(10 * 1e18)
    badger_decimals = Decimal(1e18)
    wbtc_decimals = Decimal(1e8)
    # get current reserves to see deposit ratio
    badger_balance = badger_wBTC_crv_pool.balances(0)
    wbtc_balance = badger_wBTC_crv_pool.balances(1)

    badger_normalized = Decimal(badger_balance / 1e18)
    wbtc_normalized = Decimal(wbtc_balance / 1e8)

    # We want to know how much token0 to deposit to maintain token1 levels
    test_amount_wbtc = int(Decimal(test_amount_badger / badger_decimals) * (wbtc_normalized / badger_normalized) * wbtc_decimals)

    badger.transfer(random_minter, test_amount_badger, {"from": badger_whale, "gas_price": ExponentialScalingStrategy(7, 200)})
    print(f"Transferred: {test_amount_badger} token0 {badger.balanceOf(random_minter)}")
    wBTC.transfer(random_minter, test_amount_wbtc, {"from": wbtc_whale, "gas_price": ExponentialScalingStrategy(7, 200)})
    print(f"Transferred: {test_amount_wbtc} token0 {wBTC.balanceOf(random_minter)}")

    badger.approve(badger_wBTC_crv_pool, int(test_amount_badger), {"from": random_minter, "gas_price": ExponentialScalingStrategy(7, 200)})
    wBTC.approve(badger_wBTC_crv_pool, test_amount_wbtc, {"from": random_minter, "gas_price": ExponentialScalingStrategy(7, 200)})

    now = datetime.now()
    deadline = now + timedelta(minutes=30)
    deadline_unix = deadline.timestamp()

    badger_wBTC_crv_pool.add_liquidity([int(test_amount_badger), test_amount_wbtc], deadline_unix, {"from": random_minter, "gas_price": ExponentialScalingStrategy(7, 200)})

    print(f"Deposited into curve pool: {badger_wBTC_crv_token.balanceOf(random_minter)}")
