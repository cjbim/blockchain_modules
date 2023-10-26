const { ethers, upgrades } = require("hardhat");

async function main() {
  const ERC20UpgradableV2 = await ethers.getContractFactory(
    "BARTSV2"
  );
  console.log("Upgrading BARTS...");
  await upgrades.upgradeProxy(
    "배포된 컨트랙트 주소",
    ERC20UpgradableV2
  );
  console.log("Upgraded Successfully");
}

main();
