import os
from brownie import accounts, BadgerVotingShare
from brownie.network.gas.strategies import ExponentialScalingStrategy
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_NAME = os.getenv('ACCOUNT_NAME', '')


def main():
    dev = accounts.load(ACCOUNT_NAME)

    gas_strategy = ExponentialScalingStrategy("150 gwei", "400 gwei")

    badgerVotingShare = dev.deploy(
        BadgerVotingShare, gas_price=gas_strategy, publish_source=True
    )
