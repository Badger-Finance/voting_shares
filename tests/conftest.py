from brownie import Wei
from datetime import datetime, timedelta, timezone
import pytest
from math import floor


@pytest.fixture(scope="module")
def random_digg_depositor(accounts):
    return accounts.at("0xF8dbb94608E72A3C4cEeAB4ad495ac51210a341e", force=True)


@pytest.fixture(scope="module")
def digg_whale(accounts):
    return accounts.at("0x9a13867048e01c663ce8Ce2fE0cDAE69Ff9F35E3", force=True)


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
def prep_mint_sushi(digg_whale, random_digg_depositor, digg, wBTC, digg_wBTC_SLP, sushi_router):
    test_amount_digg = Wei(1 * 1e9)
    test_amount_wbtc = Wei(1 * 1e8)
    # 25% slippage for depositing
    slippage = 0.75

    # get sushi LP reserves to see deposit ratio
    # token0 = wBTC, token1 = digg
    (reserve0, reserve1, _) = digg_wBTC_SLP.getReserves()
    wbtc_to_digg_ratio = (reserve0 / 1e8) / (reserve1 / 1e9)
    print(f'wbtc_to_digg_ratio: {wbtc_to_digg_ratio}')
    if (wbtc_to_digg_ratio > 1):
        test_amount_digg = floor(test_amount_digg / wbtc_to_digg_ratio)
    elif (wbtc_to_digg_ratio < 1):
        test_amount_wbtc = floor(test_amount_wbtc * wbtc_to_digg_ratio)
    
    print(f"Depositing {test_amount_wbtc} WBTC and {test_amount_digg} DIGG")

    now = datetime.now()
    deadline = now + timedelta(minutes=30)
    deadline_unix = deadline.timestamp()
    min_digg = test_amount_digg * slippage
    min_wbtc = test_amount_wbtc * slippage


    print(f"Transferring: {test_amount_digg} = {test_amount_digg / 1e9} DIGG")
    #  transfer 1 DIGG to deposit
    digg.transfer(random_digg_depositor, test_amount_digg * 10, {"from": digg_whale})
    print(f"Transferred: {test_amount_digg} DIGG {digg.balanceOf(random_digg_depositor)}")
    # transfer 1 wBTC to deposit
    wBTC.transfer(random_digg_depositor, test_amount_wbtc * 10, {"from": digg_whale})
    print(f"Transferred: {test_amount_wbtc} wBTC {wBTC.balanceOf(random_digg_depositor)}")

    # approve DIGG for SLP deposit
    digg.approve(sushi_router, test_amount_digg, {"from": random_digg_depositor})
    # approve wBTC for SLP deposit
    wBTC.approve(sushi_router, test_amount_wbtc, {"from": random_digg_depositor})
    # deposit
    sushi_router.addLiquidity(wBTC, digg, test_amount_wbtc, test_amount_digg, min_wbtc, min_digg, random_digg_depositor, deadline_unix, {"from": random_digg_depositor})

    print(f"Deposited to sushi, got {digg_wBTC_SLP.balanceOf(random_digg_depositor)} SLP")


@pytest.fixture(scope="module")
def prep_mint_uni(digg_whale, random_digg_depositor, digg, wBTC, digg_wBTC_UniV2, uni_router):
    test_amount_digg = Wei(1 * 1e9)
    test_amount_wbtc = Wei(1 * 1e8)
    # 25% slippage for depositing
    slippage = 0.75

    # get sushi LP reserves to see deposit ratio
    # token0 = wBTC, token1 = digg
    (reserve0, reserve1, _) = digg_wBTC_UniV2.getReserves()
    wbtc_to_digg_ratio = (reserve0 / 1e8) / (reserve1 / 1e9)
    if (wbtc_to_digg_ratio > 1):
        test_amount_digg = floor(test_amount_digg / wbtc_to_digg_ratio)
    elif (wbtc_to_digg_ratio < 1):
        test_amount_wbtc = floor(test_amount_wbtc * wbtc_to_digg_ratio)

    print(f"Depositing {test_amount_wbtc} WBTC and {test_amount_digg} DIGG")

    now = datetime.now()
    deadline = now + timedelta(minutes=30)
    deadline_unix = deadline.timestamp()
    print(f"deadline timestamp: {deadline_unix}")
    min_digg = test_amount_digg * slippage
    min_wbtc = test_amount_wbtc * slippage


    print(f"Transferring: {test_amount_digg} = {test_amount_digg / 1e9} DIGG")
    #  transfer 1 DIGG to deposit
    digg.transfer(random_digg_depositor, test_amount_digg * 10, {"from": digg_whale})
    print(f"Transferred: {test_amount_digg} DIGG {digg.balanceOf(random_digg_depositor)}")
    # transfer 1 wBTC to deposit
    wBTC.transfer(random_digg_depositor, test_amount_wbtc * 10, {"from": digg_whale})
    print(f"Transferred: {test_amount_wbtc} wBTC {wBTC.balanceOf(random_digg_depositor)}")

    # approve DIGG for SLP deposit
    digg.approve(uni_router, test_amount_digg, {"from": random_digg_depositor})
    # approve wBTC for SLP deposit
    wBTC.approve(uni_router, test_amount_wbtc, {"from": random_digg_depositor})
    # deposit
    uni_router.addLiquidity(wBTC, digg, test_amount_wbtc, test_amount_digg, min_wbtc, min_digg, random_digg_depositor, deadline_unix, {"from": random_digg_depositor})

    print(f"Deposited to uni, got {digg_wBTC_UniV2.balanceOf(random_digg_depositor)} UniV2")


@pytest.fixture(scope="module")
def digg_voter(DiggVotingShare, random_digg_depositor):
    diggVotingShare = random_digg_depositor.deploy(DiggVotingShare)
    return diggVotingShare
