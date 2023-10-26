# erc20_upgrable
hardhat을 이용한 업그레이드 가능한 erc-20 계약 배포및 테스트 <br>
npm install <br>
.env 에서 체인 네트워크와 지갑 개인키 등록 <br>
배포 <br>
npx hardhat run scripts/deploy.js --network testnet <br>
업그레이드된 컨트랙트 배포 <br>
npx hardhat run scripts/upgrade.js --network testnet <br>
테스트는 web3 py 에서 진행
