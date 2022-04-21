/**
 * @type import('hardhat/config').HardhatUserConfig
 */

require('hardhat-deploy');

module.exports = {
  solidity: "0.8.7",
  networks: {
    arbitrum: {
      url: "https://arb-mainnet.g.alchemy.com/v2/$ARB_ALCHEMY_URL",
      chainId: 42161,
      verify: {
        etherscan: {
          apiUrl: "https://api.arbiscan.io/api",
          apiKey: "$ARBISCAN_API_KEY"
        }
      }
    }
  }
};
