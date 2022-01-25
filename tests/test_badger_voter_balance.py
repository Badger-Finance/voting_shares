from brownie import Wei

def test_badger_sett_balance(prep_mint_bBadger, badger_voter, random_minter, badger):
    amount_deposited = Wei(1)
    balance = badger_voter.badgerBalanceOf(random_minter) - badger.balanceOf(random_minter)
    balance_normalized = balance / 1e18

    print(f'badger balance: {balance_normalized} = {amount_deposited}')

    assert abs(balance_normalized - amount_deposited) <= 1e-6


def test_rari_voter_balance(badger_voter, prep_mint_fBadger, random_minter):
    amount_minted = Wei("100 ether")
    balance = badger_voter.rariBalanceOf(random_minter)

    print(f"balance={balance.to('ether')}")

    assert amount_minted == balance


def test_uni_voter_balance(prep_mint_badger_uni, badger_voter, random_minter, badger_wBTC_univ2):
    amount_deposited = 1
    balance = badger_voter.uniswapBalanceOf(random_minter)
    balance_normalized = balance / 1e18

    print(f'uni balance: {balance_normalized}')

    assert abs(balance_normalized - amount_deposited) < 1e-3


def test_sushi_voter_balance(prep_mint_badger_sushi, badger_voter, random_minter, badger_wBTC_SLP):
    amount_deposited = 1
    balance = badger_voter.uniswapBalanceOf(random_minter)
    balance_normalized = balance / 1e18

    print(f'uni balance: {balance_normalized}')

    assert abs(balance_normalized - amount_deposited) < 1e-3