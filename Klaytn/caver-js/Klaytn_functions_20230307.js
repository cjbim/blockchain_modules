
/* 
    date = 2023 - 03 - 02
    network verify 추가
    getBalance 추가
    date = 2023-03-07
    kaikas 지갑 호출 불가 이슈 해결
    예상 : 이미 wallet connect에서 window. 이 이미 전역을 선언 되어있어서 호출 함수에 window가 또 넣었기 때문에 
    전역 객체가 겹쳐 져서 호출 함수 내부에 데이터가 비워진 데이터를 받아서 이슈가 발생
    해결 : 내부 함수에 window 제거 
*/
const Caver = require('caver-js');
function Klaytn_network(network) {
    let caver;
    if (network == 'baobab') {
        caver = new Caver('https://api.baobab.klaytn.net:8651/'); //테스트넷
    } else if (network == 'ganache') {
        caver = new Caver('http://localhost:8545'); //테스트넷
    } else if (network == 'klaytn') {
        caver = new Caver('https://public-node-api.klaytnapi.com/v1/cypress'); // 메인넷
    } else {
        caver = new Caver('https://api.baobab.klaytn.net:8651/'); //테스트넷
    }
    return caver;
};

async function Klaytn_network_verify(caver) {
    const verify = await caver.klay.getChainId()
    let check_network = "unknown"
    if (verify == 1001) {
        check_network = "baobab"
        console.log("baobab")
    } else if (verify == 8217){
        check_network = "klaytn"
        console.log("klaytn")
    }else {
        console.log("unknown")
    }
    return check_network;
};



/*----------------코인파트-----------------------*/

async function Klaytn_getbalance(caver, address){
    address = caver.utils.toChecksumAddress(address)
    let balance = caver.utils.fromPeb(await caver.klay.getBalance(address), 'KLAY')
    console.log(balance)
    return balance
}

async function Klaytn_klay_transfer(caver,sender,receiver,amt){
    /*
    caver: network
    sender: 보내는사람 (연결된지갑 에서 가져옴)
    receiver: 받는사람 (유저가 직접입력 받은걸 가져옴 아니면 고정값)
    amt: 보낼 값 (입력받거나 고정값)
    */
    sender = caver.utils.toChecksumAddress(sender)
    receiver = caver.utils.toChecksumAddress(receiver)
    let Amt = amt * caver.utils.toPeb('1', 'KLAY') //이유 = 소수들어 가면 에러나기 때문에 미리 단위 변환 하고 삽입
    console.log(Amt)
    console.log(receiver)

    const transferKlay = await caver.klay.sendTransaction({
        type: 'VALUE_TRANSFER',
        from: sender,
        to: receiver,
        value: caver.utils.toBN(Amt),
        gas: 8000000
     })
     .once('transactionHash', transactionHash => {
        console.log('txHash', transactionHash);
     })
     .once('receipt', receipt => {
        console.log('receipt', receipt);
     })
     .once('error', error => {
        console.log('error', error);
        alert("지불에 실패하셨습니다.");
     })

     return transferKlay
}

async function sign(caver,message,account){
    sender = caver.utils.toChecksumAddress(account)
    const signedMessage = await caver.klay.sign(message, account)
    return signedMessage
}


/*----------------NFT파트-----------------------*/

async function Klaytn_Kip17_deploy(caver,sender,name,symbol){
    /*
    기능 : kip-17 컨트랙트 배포
    caver = 네트워크
    sender = 현재 연결된 유저 (배포자)
    name = NFT 컨트랙트 이름
    symbol  = 짧은 이름
    */
    sender = caver.utils.toChecksumAddress(sender)
    let tx = await caver.klay.KIP17.deploy({
        name: name,
        symbol: symbol,
    }, sender)
    console.log(tx._address)

    return tx._address
 }

 async function Klaytn_Kip17_contract_abi(caver,contract_address){
    /*
    기능 : 배포된 컨트랙트 abi불러오기
    caver = 네트워크
    contract_address = 배포된 컨트랙트 주소
    */
    contract_address = caver.utils.toChecksumAddress(contract_address)
    const kip17Instance  = new caver.klay.KIP17(contract_address)
    return kip17Instance
 }

 async function Klaytn_Kip17_mint_NFT(caver,kip17Instance,sender,tokenURI){
    /*
    기능 : 배포된 컨트랙트 에서 NFT 발행
    caver = 네트워크
    kip17Instance = ABI
    sender = 현재 연결된 컨트랙트 주인
    tokenURI = 발행할 NFT 메타데이터
    */
    sender = caver.utils.toChecksumAddress(sender)
    let token_id =await kip17Instance.totalSupply()
    let new_token_id = parseInt(token_id)+1
    let inputdata = await kip17Instance.mintWithTokenURI(sender, new_token_id, tokenURI,{ from: sender })
    return inputdata
    

 }

 async function Klaytn_Kip17_approve(caver,kip17Instance,sender,receiver,tokenid){
    /*
    기능 : 배포된 컨트랙트 에서 특정 NFT에 대한 권한 주기
    caver = 네트워크
    kip17Instance = ABI
    sender = 현재 연결된 컨트랙트 주인
    receiver = 권한을 받을 사람
    tokenid = 권한을 줄 토큰 ID
    */
    sender = caver.utils.toChecksumAddress(sender)
    receiver = caver.utils.toChecksumAddress(receiver)
    let appv = await kip17Instance.approve(receiver, tokenid, { from: sender })
    return appv
 }

 async function Klaytn_Kip17_NFT_transfer(caver,kip17Instance,sender,receiver,tokenid){
     /*
    기능 : NFT 보내기
    caver = 네트워크
    kip17Instance = ABI
    sender = 현재 연결된 컨트랙트 주인
    receiver = 받을 사람
    tokenid = 보내줄 토큰 ID
    */
    sender = caver.utils.toChecksumAddress(sender)
    receiver = caver.utils.toChecksumAddress(receiver)
    let tx = await kip17Instance.safeTransferFrom(sender, receiver, tokenid, { from: sender })
    return tx
 }

 async function Klaytn_Kip17_NFT_burn(caver,kip17Instance,sender,tokenid){
    /*
    기능 : 컨트랙트에 배포된 NFT 삭제 시키기
    caver = 네트워크
    kip17Instance = ABI
    sender = 현재 연결된 컨트랙트 주인
    tokenid = 삭제할 NFT 토큰 ID
    */
    sender = caver.utils.toChecksumAddress(sender)
    let burning = await kip17Instance.burn(tokenid, { from: sender })
    return burning
 }
async function Klaytn_Kip17_pause(caver,kip17Instance,sender){
     /*
    기능 : 토큰 전송과 관련된 기능들을 중지
    caver = 네트워크
    kip17Instance = ABI
    sender = 현재 연결된 컨트랙트 주인
    */
    sender = caver.utils.toChecksumAddress(sender)
    let pauser = await kip17Instance.pause({ from: sender})
    return pauser
}
async function Klaytn_Kip17_unpause(caver,kip17Instance,sender){
     /*
    기능 : 토큰 전송과 관련된 기능들을 중지 해제
    caver = 네트워크
    kip17Instance = ABI
    sender = 현재 연결된 컨트랙트 주인
    */
    sender = caver.utils.toChecksumAddress(sender)
    let unpauser = await kip17Instance.unpause({ from: sender })
    return unpauser
}


/*----------------Token파트-----------------------*/


async function Klaytn_Kip7_deploy(caver,sender,name,symbol,supply){ //2022-10-06 테스트 진행중
    /*
    기능 : kip-7 토큰 배포
    caver = 네트워크
    sender = 발행자
    name = 토큰 이름
    symbol = 토큰 심볼
    supply = 발행량
    */
    sender = caver.utils.toChecksumAddress(sender)
    let total = supply * caver.utils.toPeb(1, 'KLAY')
    
    let tx = await caver.klay.KIP7.deploy({
        name: name,
        symbol: symbol,
        decimals: 18,
        initialSupply: total,
        },sender)
    console.log(tx._address)

    return tx._address

 }

async function Klaytn_Kip7_contract_abi(caver,contract_address){
    /*
    기능 : 배포된 컨트랙트 abi불러오기
    caver = 네트워크
    contract_address = 배포된 컨트랙트 주소
    */
    contract_address = caver.utils.toChecksumAddress(contract_address)
    const kip7Instance  = new caver.klay.KIP7(contract_address)
    return kip7Instance
 }

async function Klaytn_Kip7_get_balance(caver,kip7Instance,owner){
    /*
    기능 : 계정의 토큰이 얼마 있는지 확인한다
    caver = 네트워크
    kip7Instance = 컨트랙트 abi    
    owner = 확인할 지갑 address 
    */
    owner = caver.utils.toChecksumAddress(owner)

    let balance = await kip7Instance.balanceOf(owner).then(console.log)
    return balance
 }

async function Klaytn_Kip7_totalSupply(caver,kip7Instance){
    /*
    기능 : 토큰의 총발행량 확인
    caver = 네트워크
    kip7Instance = 컨트랙트 abi     
    */
    let total = await kip7Instance.totalSupply().then(console.log)
    return total
 }


async function Klaytn_Kip7_token_transfer(caver,kip7Instance,owner,receiver,amt){
    /*
    기능 : 토큰 보내기
    caver = 네트워크
    kip7Instance = 컨트랙트 abi     
    owner = 보내는 사람
    receiver = 받는 사람 
    amt = 보내는 토큰의 갯수
    */
    owner = caver.utils.toChecksumAddress(owner)
    receiver = caver.utils.toChecksumAddress(receiver)
    let transfer = await kip7Instance.transfer(receiver, amt, { from: owner })
    return transfer
 }
/*
async function Klaytn_Kip7_approve(caver,kip7Instance,owner,receiver,amt){
    
    기능 : 토큰 소유자의 토큰을 owner가 amount만큼 사용하도록 허락합니다
    caver = 네트워크
    kip7Instance = 컨트랙트 abi     
    owner = 주인
    receiver = 허락받을 자 
    amt = 허락받을 토큰의 갯수
    사용금지 : 이유 컨트랙트에 권한을 이양하는 용도 이기 때문에 사용할 필요가 없다.
    owner = caver.utils.toChecksumAddress(owner)
    receiver = caver.utils.toChecksumAddress(receiver)
    let approver = await kip7Instance.approve(receiver, amt, { from: owner })
    return approver

 }
 */
 async function Klaytn_Kip7_token_mint(caver,kip7Instance,owner,amt){
    /*
    기능 : amt만큼 토큰을 만들어 account에게 발행합니다. 이 함수는 토큰 총 공급량을 증가시킵니다.
    caver = 네트워크
    kip7Instance = 컨트랙트 abi     
    owner = 주인
    amt = 추가발행 토큰의 갯수
    */
    owner = caver.utils.toChecksumAddress(owner)
    let minter = await kip7Instance.mint(owner, amt, { from: owner }) // 1번 파라미터에 다른 계정의 주소넣어도 가능하다 
    return minter
 }

async function Klaytn_Kip7_burn(caver,kip7Instance,owner,amt){
    /*
    기능 : 토큰을 burn 시킵니다
    caver = 네트워크
    kip7Instance = 컨트랙트 abi     
    owner = 주인
    amt = burn할 토큰의 갯수
    */
    cowner = caver.utils.toChecksumAddress(owner)
    let burning = await kip7Instance.burn(amt, { from: owner })
 }

async function Klaytn_Kip7_pause(caver,kip7Instance,owner){
    /*
    기능 : 토큰 전송과 관련된 기능들을 중지합니다.
    caver = 네트워크
    kip7Instance = 컨트랙트 abi     
    owner = 주인
    */
    owner = caver.utils.toChecksumAddress(owner)
    let pauser = await kip7Instance.pause( {from: owner })
    return pauser
}
async function Klaytn_Kip7_unpause(caver,kip7Instance,owner){
    /*
    기능 : 중지된 컨트랙트를 재개합니다.
    caver = 네트워크
    kip7Instance = 컨트랙트 abi     
    owner = 주인
    */
    owner = caver.utils.toChecksumAddress(owner)
    let unpauser = await kip7Instance.unpause({ from: owner})
    return unpauser
}