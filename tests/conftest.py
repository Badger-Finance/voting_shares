from brownie import Wei
from datetime import datetime, timedelta
import pytest


########### GENERAL FIXTURES ###########

@pytest.fixture(scope="module")
def wbtc_whale(accounts):
    return accounts.at("0x176f3dab24a159341c0509bb36b833e7fdd0a132", force=True)

########### DIGG FIXTURES ###########

@pytest.fixture(scope="module")
def random_digg_depositor(accounts):
    return accounts.at("0xF8dbb94608E72A3C4cEeAB4ad495ac51210a341e", force=True)

@pytest.fixture(scope="module")
def digg_whale(accounts):
    return accounts.at("0x4a8651F2edD68850B944AD93f2c67af817F39F62", force=True)

@pytest.fixture(scope="module")
def fDigg(interface):
    return interface.ICToken("0x792a676dD661E2c182435aaEfC806F1d4abdC486")

@pytest.fixture(scope="module")
def digg(interface):
    return interface.IERC20("0x798d1be841a82a273720ce31c822c61a67a601c3")

@pytest.fixture(scope="module")
def wBTC(interface):
    return interface.IERC20("0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599")

@pytest.fixture(scope="module")
def digg_wBTC_UniV2(interface):
    return interface.IUniswapV2Pair("0xE86204c4eDDd2f70eE00EAd6805f917671F56c52")

@pytest.fixture(scope="module")
def digg_wBTC_SLP(interface):
    return interface.IUniswapV2Pair("0x9a13867048e01c663ce8Ce2fE0cDAE69Ff9F35E3")

@pytest.fixture(scope="module")
def sushi_router(interface):
    return interface.IUniswapV2Router01("0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F")

@pytest.fixture(scope="module")
def uni_router(interface):
    return interface.IUniswapV2Router01("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")

@pytest.fixture(scope="module")
def digg_sett(interface):
    return interface.ISett("0x7e7E112A68d8D2E221E11047a72fFC1065c38e1a")


########### BADGER FIXTURES ###########

@pytest.fixture(scope="module")
def random_minter(accounts):
    yield accounts.at("0xF8dbb94608E72A3C4cEeAB4ad495ac51210a341e", force=True)

@pytest.fixture(scope="module")
def badger_whale(accounts):
    yield accounts.at("0x4441776e6A5D61fA024A5117bfc26b953Ad1f425", force=True)

@pytest.fixture(scope="module")
def fBadger(interface):
    yield interface.ICToken("0x6780B4681aa8efE530d075897B3a4ff6cA5ed807")

@pytest.fixture(scope="module")
def badger_wBTC_univ2(interface):
    return interface.IUniswapV2Pair("0xcd7989894bc033581532d2cd88da5db0a4b12859")

@pytest.fixture(scope="module")
def badger_wBTC_SLP(interface):
    return interface.IUniswapV2Pair("0x110492b31c59716ac47337e616804e3e3adc0b4a")

@pytest.fixture(scope="module")
def badger_sett(interface):
    return interface.ISett("0x19D97D8fA813EE2f51aD4B4e04EA08bAf4DFfC28")

@pytest.fixture(scope="module")
def badger(interface):
    yield interface.IERC20("0x3472A5A71965499acd81997a54BBA8D852C6E53d")


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
    token1.transfer(depositor, test_amount_token1, {"from": whale[token1]})
    print(f"Transferred: {test_amount_token1} token1 {token1.balanceOf(depositor)}")
    # transfer token0 to deposit
    token0.transfer(depositor, test_amount_token0, {"from": whale[token0]})
    print(f"Transferred: {test_amount_token0} token0 {token0.balanceOf(depositor)}")

    # approve token1 for deposit
    token1.approve(router, test_amount_token1, {"from": depositor})
    # approve token0 for deposit
    token0.approve(router, test_amount_token0, {"from": depositor})
    # deposit
    router.addLiquidity(token0, token1, test_amount_token0, test_amount_token1, min_token0, min_token1, depositor, deadline_unix, {"from": depositor})


########### DIGG TEST SETUP ###########

@pytest.fixture(scope="module")
def prep_mint_bDigg(digg_whale, random_digg_depositor, digg, digg_sett):
    test_amount = 1*1e9
    print(f"Transferring: {test_amount} = {test_amount / 1e9} DIGG")
    #  transfer 1 DIGG to minter
    digg.transfer(random_digg_depositor, test_amount, {"from": digg_whale})
    print(f"Transferred: {test_amount} DIGG {digg.balanceOf(random_digg_depositor)}")

    # approve DIGG for deposit into vault
    digg.approve(digg_sett, test_amount, {"from": random_digg_depositor})
    # deposit into vault
    digg_sett.deposit(test_amount, {"from": random_digg_depositor})

    digg_sett_balance = digg_sett.balanceOf(random_digg_depositor)
    print(f"bDIGG received: {digg_sett_balance}")
    digg_ppfs = digg_sett.balance() / digg_sett.totalSupply()
    print(f"Converts to: {digg_sett_balance * digg_ppfs / 1e9} deposited digg")

@pytest.fixture(scope="module")
def prep_mint_fDigg(digg_whale, random_digg_depositor, digg, fDigg):
    test_amount = 1*1e9
    print(f"Transferring: {test_amount} = {test_amount / 1e9} DIGG")
    #  transfer 1 DIGG to minter
    digg.transfer(random_digg_depositor, test_amount, {"from": digg_whale})
    print(f"Transferred: {test_amount} DIGG {digg.balanceOf(random_digg_depositor)}")

    # approve DIGG for minting
    digg.approve(fDigg, test_amount, {"from": random_digg_depositor})
    # mint
    fDigg.mint(test_amount, {"from": random_digg_depositor})
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
    diggVotingShare = random_digg_depositor.deploy(DiggVotingShare)
    return diggVotingShare


########### BADGER TEST SETUP ###########

@pytest.fixture(scope="module")
def prep_mint_bBadger(badger_whale, random_minter, badger, badger_sett):
    test_amount = 1 * 1e18
    print(f"Transferring: {test_amount} = {test_amount / 1e18} BADGER")
    #  transfer 1 BADGER to minter
    badger.transfer(random_minter, test_amount, {"from": badger_whale})
    print(f"Transferred: {test_amount} BADGER = {badger.balanceOf(random_minter)}")

    # approve BADGER for deposit into vault
    badger.approve(badger_sett, test_amount, {"from": random_minter})
    # deposit into vault
    badger_sett.deposit(test_amount, {"from": random_minter})

    badger_sett_balance = badger_sett.balanceOf(random_minter)
    print(f"bBadger received: {badger_sett_balance}")
    badger_ppfs = badger_sett.balance() / badger_sett.totalSupply()
    print(f"Converts to: {badger_sett_balance * badger_ppfs / 1e18} deposited badger")

@pytest.fixture(scope="module")
def prep_mint_fBadger(badger_whale, random_minter, badger, fBadger):
    test_amount = Wei("100 ether")
    #  transfer from whale to 1000 BADGER
    badger.transfer(random_minter, test_amount, {"from": badger_whale})
    # approve BADGER for minting
    badger.approve(fBadger, test_amount, {"from": random_minter})
    #  mint
    fBadger.mint(test_amount, {"from": random_minter})

@pytest.fixture(scope="module")
def badger_voter(BadgerVotingShare, random_minter):
    badgerVotingShare = random_minter.deploy(BadgerVotingShare)
    yield badgerVotingShare

@pytest.fixture(scope="module")
def prep_mint_badger_uni(badger_whale, wbtc_whale, random_minter, badger, wBTC, badger_wBTC_univ2, uni_router):
    univ2_deposit(badger_wBTC_univ2, wBTC, 1e8, badger, 1e18, 1, uni_router, random_minter, {badger: badger_whale, wBTC: wbtc_whale})
    print(f"Deposited to uni, got {badger_wBTC_univ2.balanceOf(random_minter)} UniV2")

@pytest.fixture(scope="module")
def prep_mint_badger_sushi(badger_whale, wbtc_whale, random_minter, badger, wBTC, badger_wBTC_SLP, sushi_router):
    univ2_deposit(badger_wBTC_SLP, wBTC, 1e8, badger, 1e18, 1, sushi_router, random_minter, {badger: badger_whale, wBTC: wbtc_whale})
    print(f"Deposited to sushi, got {badger_wBTC_SLP.balanceOf(random_minter)} SLP")