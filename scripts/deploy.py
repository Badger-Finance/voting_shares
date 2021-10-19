from brownie import accounts, BadgerVotingShare
from brownie.network.gas.strategies import ExponentialScalingStrategy


ACCOUNT_NAME = ""


def main():
    dev = accounts.load(ACCOUNT_NAME)

    gas_strategy = ExponentialScalingStrategy("75gwei", "110 gwei")

    badgerVotingShare = dev.deploy(
        BadgerVotingShare, gas_price=gas_strategy, publish_source=True
    )
