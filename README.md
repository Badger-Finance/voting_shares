
Run test:
Tests are scoped by network, in order to run the full test suite you'll need to run for both Arbitrum and Eth Mainnet
```
brownie test --network=mainnet-fork
brownie test --network=arbitrum-fork
```

Deploy:

The commands below use conventional naming for brownie, you can check your network names by running:
`brownie networks list`
and choosing the network name that corresponds with the network you would like to deploy on.

Eth Mainnet Badger Voting Share:
`brownie run scripts/deploy_badger.py --network=mainnet`

Eth Mainnet Digg Voting Share:
`brownie run scripts/deploy_digg.py --network=mainnet`

Arb Mainnet Badger Voting Share:
`brownie run scripts/deploy_badger_arb.py --network=arbitrum`
