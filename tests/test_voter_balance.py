from brownie import Wei
from pytest import approx
import math


def test_rari_voter_balance(prep_mint_fDigg, digg_voter, random_depositor):
    amount_minted = 1
    print(f"Amount minted: {amount_minted}")
    balance = digg_voter.rariBalanceOf(random_depositor)
    balance_normalized = balance / 1e9
    print(f"balance={balance_normalized}")

    assert abs(balance_normalized - amount_minted) < 1e-6

def test_sushi_voter_balance(prep_mint_sushi, digg_voter, random_depositor, digg_wBTC_SLP):
    (reserve0, reserve1, _) = digg_wBTC_SLP.getReserves()
    wbtc_to_digg_ratio = (reserve0 / 1e8) / (reserve1 / 1e9)
    if (wbtc_to_digg_ratio > 1):
        amount_deposited = 1 / wbtc_to_digg_ratio
    else:
        amount_deposited = 1
    
    balance = digg_voter.sushiswapBalanceOf(random_depositor)
    balance_normalized = balance / 1e9
    print(f"sushi balance: {balance_normalized}")

    assert abs(balance_normalized - amount_deposited) < 1e-6

def test_uni_voter_balance(prep_mint_uni, digg_voter, random_depositor, digg_wBTC_UniV2):
    (reserve0, reserve1, _) = digg_wBTC_UniV2.getReserves()
    wbtc_to_digg_ratio = (reserve0 / 1e8) / (reserve1 / 1e9)
    if (wbtc_to_digg_ratio > 1):
        amount_deposited = 1 / wbtc_to_digg_ratio
    else:
        amount_deposited = 1
    print(f"Amount deposited: {amount_deposited}")
    balance = digg_voter.uniswapBalanceOf(random_depositor)
    balance_normalized = balance / 1e9

    print(f"uni balance: {balance_normalized}")

    assert abs(balance_normalized - amount_deposited) < 1e-6

def test_digg_sett_balance(prep_mint_bDigg, digg_voter, random_depositor):
    amount_deposited = Wei(1)
    balance = digg_voter.diggBalanceOf(random_depositor)
    balance_normalized = balance / 1e9

    print(f"digg balance: {balance_normalized} = {amount_deposited}")

    assert abs(balance_normalized - amount_deposited) < 1e-6

