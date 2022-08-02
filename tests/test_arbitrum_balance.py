from brownie import Wei
import pytest


@pytest.mark.require_network("arb-main-fork")
def test_badger_sett_balance(prep_mint_arb_badger, random_minter, arb_badger_voter):
    amount_deposited = Wei(1)
    balance = arb_badger_voter.badgerBalanceOf(random_minter)
    balance_normalized = balance / 1e18

    print(f"badger balance: {balance_normalized} = {amount_deposited}")

    assert abs(balance_normalized - amount_deposited) <= 1e-6


@pytest.mark.require_network("arb-main-fork")
def test_swapr_voter_balance(prep_mint_arb_swapr, arb_badger_voter, random_minter):
    amount_deposited = 1
    balance = arb_badger_voter.swaprBalanceOf(random_minter)
    balance_normalized = balance / 1e18

    print(f"swapr balance: {balance_normalized}")

    assert abs(balance_normalized - amount_deposited) < 1e-3
