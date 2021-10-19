from brownie import Wei
import pytest


@pytest.fixture(scope="module")
def random_minter(accounts):
    yield accounts.at("0xF8dbb94608E72A3C4cEeAB4ad495ac51210a341e", force=True)


@pytest.fixture(scope="module")
def badger_whale(accounts):
    yield accounts.at("0xc2Be79CF419CF48f447320D5D16f5115bBb58B03", force=True)


@pytest.fixture(scope="module")
def fBadger(interface):
    yield interface.ICToken("0x6780B4681aa8efE530d075897B3a4ff6cA5ed807")


@pytest.fixture(scope="module")
def badger(interface):
    yield interface.IERC20("0x3472A5A71965499acd81997a54BBA8D852C6E53d")


@pytest.fixture(scope="module")
def prep_mint_fBadger(badger_whale, random_minter, badger, fBadger):
    test_amount = Wei("100 ether")
    #  transfer from whale to 1000 BADGER
    badger.transfer(random_minter, test_amount, {"from": badger_whale})
    # approve BADGER for minting
    badger.approve(fBadger, test_amount, {"from": random_minter})
    #  mint
    fBadger.mint(test_amount, {"from": random_minter})


@pytest.fixture(scope="module")
def badger_voter(BadgerVotingShare, random_minter):
    badgerVotingShare = random_minter.deploy(BadgerVotingShare)
    yield badgerVotingShare
