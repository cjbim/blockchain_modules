require("@nomiclabs/hardhat-ethers");
require("@openzeppelin/hardhat-upgrades");
require("dotenv").config();

module.exports = {
  solidity: "0.8.7",
  networks: {
    testnet: {
      url: process.env.URL,
      accounts: [process.env.PRIVATE_KEY],
    },
  },
};
