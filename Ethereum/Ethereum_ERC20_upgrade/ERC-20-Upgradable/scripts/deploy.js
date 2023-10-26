const { ethers, upgrades } = require("hardhat");


async function main() {
  const ERC20UpgradableV1 = await ethers.getContractFactory(
    "BARTS"
  );
  
  
  console.log("Deploying Barts...");
  const contract = await upgrades.deployProxy(ERC20UpgradableV1, ["0x6A123F6C4fdae27995872d7961C74102a16eD27e"], {
    initializer: "initialize",
    kind: "transparent",
  });
  await contract.deployed();
  console.log("Barts deployed to:", contract.address);
}

main();