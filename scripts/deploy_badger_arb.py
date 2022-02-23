import os
from brownie import accounts, ArbBadgerVotingShare
from brownie.network.gas.strategies import ExponentialScalingStrategy
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_NAME = os.getenv('ACCOUNT_NAME', '')


def main():
    dev = accounts.load(ACCOUNT_NAME)

    gas_strategy = ExponentialScalingStrategy("2 gwei", "10 gwei")

    badgerVotingShare = dev.deploy(
        ArbBadgerVotingShare, gas_price=gas_strategy, publish_source=True
    )
