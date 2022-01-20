from brownie import Wei


def test_rari_voter_balance(badger_voter, prep_mint_fBadger, random_minter):
    amount_minted = Wei("100 ether")
    balance = badger_voter.balanceOf(random_minter)

    print(f"balance={balance.to('ether')}")

    assert amount_minted == balance