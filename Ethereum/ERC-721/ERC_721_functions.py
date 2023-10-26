from web3 import Web3, HTTPProvider
import json
import solcx
import datetime
import os
import urllib
version = solcx.install_solc('0.8.9') # 최초 1회에만 사용
'''
2023-04-20
baseuri 사용으로 estimate_gas 240000 -> 150000 약 9만 절약
access controll 와 ownable 을 같이 사용이 불가 하여
klaytn 에서 사용하던 minter_role 이식해서 사용


'''
###### 공용 함수 영역 #####


def ethereum_connectWeb3(infura_api_key, connect_host=None):

	if connect_host is None:
		infura_url = "http://222.231.30.70:8041"
	elif connect_host == "mainnet":
		infura_url = "https://mainnet.infura.io/v3/"+infura_api_key
	elif connect_host == "goerli":
		infura_url = "https://goerli.infura.io/v3/"+infura_api_key
	elif connect_host == "gnctest":
		infura_url = "http://222.231.30.70:8041"
	elif connect_host == "gnceth":		#훗날에 바꿔야함 20230109
		infura_url = "http://222.231.30.70:8041"
	else:
		infura_url = "http://localhost:8545"
	web3 = Web3(Web3.HTTPProvider(infura_url))
	print(f"{infura_url} connect is {web3.is_connected()}")
	return web3

def ethereum_check_network(web3):
    check = web3.net.version
    if check == "1":
        network = "mainnet"
    elif check == "5":
        network = "goerli"
    else:
        network = "Unknown"

    return network

def ethereum_etherscan_link(network, contract_address):
    if network == "mainnet":
        url = f"https://etherscan.io/address/{contract_address}"
    elif network == "goerli":
        url = f"https://goerli.etherscan.io/address/{contract_address}"
    else:
        url = "unknown"

    return url
def ethereum_getBalance(web3, account):
	account = web3.to_checksum_address(account)
	balance = web3.from_wei(web3.eth.get_balance(account), 'ether')
	return balance

def ethereum_read_abi(file_name):
	with open(file_name) as f:
		info_json = json.load(f)
	return info_json["abi"]

def ethereum_getContract(web3, contractAddress, contractAbi):
	file = open(contractAbi, 'r', encoding='utf-8')
	contractaddress = web3.to_checksum_address(contractAddress)
	mycontract = web3.eth.contract(abi=file.read(), address=contractaddress)
	return mycontract


##### 트랜잭션 영역 #####
# 수수료 소모 #
##############################################
def ethereum_erc721_contract_deploy(web3, file_path, address, pk_key,name,symbol,base_uri,new_add):
    '''
    컨트랙트 배포 함수
    :param web3: 이더리움 네트워크
    :param file_path: sol파일 경로
    :param address: 배포하는 사람의 주소값
    :param pk_[key: 배포하는 사람의 pk값
    :param name: 컨트랙트 이름
    :param symbol: 컨트랙트 심볼
    :return: 컨트랙트 주소
    '''
    res = solcx.compile_files(
        [file_path],
        output_values=["abi", "bin"],
        solc_version="0.8.9"
    )
    print(res)
    abi = res[file_path+':MyNFT']['abi']
    with open(f'./{name}abi', 'w') as f:
        json.dump(abi, f)
    bin = res[file_path+':MyNFT']['bin']
    #with open(f'{name}bin', 'w') as f:-
    #    json.dump(bin, f)
    mycontract = web3.eth.contract(abi=abi, bytecode=bin)
    address = web3.to_checksum_address(address)
    own_add = web3.to_checksum_address(new_add)
    #acct = web3.eth.accounts.privateKeyToAccount(pk_key)
    acct = web3.eth.account.from_key(pk_key)
    nonce = web3.eth.get_transaction_count(address)
    gas_price = web3.eth.gas_price
    print(gas_price)
    tx = mycontract.constructor( name, symbol,base_uri,own_add).build_transaction(
        {
            "from": address,
            "nonce": nonce,
            "gasPrice": gas_price+ web3.to_wei(2, 'gwei')
        }
    )
    signed = acct.signTransaction(tx)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress



def ethereum_erc721a_mint(web3,erc721_contract, owner_add, owner_pk,total, nft_owner_add):
    '''
    NFT mint 함수
    :param web3: 이더리움 네트워크
    :param erc721_contract: abi로 활성화한 컨트랙트 함수들
    :param owner_add: minter의 주소 값
    :param owner_pk: minter의 개인키 값
    :param total: 발행할 수량
    :return: gncHash
    '''

    owner_add = web3.to_checksum_address(owner_add)

    nonce = web3.eth.get_transaction_count(owner_add)

    gas_estimate = erc721_contract.functions.mint(nft_owner_add,total).estimate_gas({'from': owner_add})
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(web3.to_wei(gas_price, 'gwei'))
    print(f"txfee: {web3.from_wei(gas_estimate * gas_price, 'Ether')}")
    tx = erc721_contract.functions.mint(nft_owner_add,total).build_transaction(
        {
            'from': owner_add,
            'nonce': nonce,
            'gas': gas_estimate *2,
            "gasPrice": gas_price+ web3.to_wei(2, 'gwei')
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, owner_pk)
    amtTxHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(amtTxHash)
    return gncHash




def ethereum_erc721a_set_baseuri(web3,mycontract,add,pv,newbaseuri):
    '''
    contract baseuri 변경 함수 (주의)
    :param web3: 이더리움 네트워크
    :param mycontract: abi로 활성화한 컨트랙트 함수들
    :param add: minter의 주소 값
    :param pv: minter의 개인키 값
    :param newbaseuri: 새롭게 세팅할 baseuri 값
    :return: gncHash
    '''
    owner_add = web3.to_checksum_address(add)
    nonce = web3.eth.get_transaction_count(add)

    gas_estimate = mycontract.functions.setBaseURI(newbaseuri).estimate_gas({'from': owner_add})
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(web3.to_wei(gas_price, 'gwei'))
    print(f"txfee: {web3.from_wei(gas_estimate * gas_price, 'Ether')}")
    tx = mycontract.functions.setBaseURI(newbaseuri).build_transaction(
        {
            'from': owner_add,
            'nonce': nonce,
            'gas': gas_estimate *2,
            "gasPrice": gas_price+ web3.to_wei(2, 'gwei')
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, pv)
    amtTxHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(amtTxHash)
    return gncHash

def ethereum_erc721a_add_minter(web3,mycontract,add,pv,new_minter_add):
    '''
    mint 권한을 주는 함수 (주의)
    :param web3: 이더리움 네트워크
    :param mycontract: abi로 활성화한 컨트랙트 함수들
    :param add: minter의 주소 값
    :param pv: minter의 개인키 값
    :param new_minter_add: 새로운 minter의 주소값
    :return: gncHash
    '''
    owner_add = web3.to_checksum_address(add)
    new_minter_address = web3.to_checksum_address(new_minter_add)
    nonce = web3.eth.get_transaction_count(add)

    gas_estimate = mycontract.functions.addMinter(new_minter_address).estimate_gas({'from': owner_add})
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(web3.to_wei(gas_price, 'gwei'))
    print(f"txfee: {web3.from_wei(gas_estimate * gas_price, 'Ether')}")
    tx = mycontract.functions.addMinter(new_minter_address).build_transaction(
        {
            'from': owner_add,
            'nonce': nonce,
            'gas': gas_estimate *2,
            "gasPrice": gas_price+ web3.to_wei(2, 'gwei')
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, pv)
    amtTxHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(amtTxHash)
    return gncHash

def ethereum_erc721a_renounceMinter(web3, mycontract, owner_add, owner_pv):
    '''
    minter 권한을 가진 add를 minter 권한을 박탈하는 함수(주의: minter가 한명이면 다른 주소로 넘겨주고 실행 해야함 안그러면 벽돌될 가능성 농훈)
    :param web3: 이더리움 네트워크
    :param mycontract: abi로 활성화한 컨트랙트 함수들
    :param add: minter의 주소 값
    :param pv: minter의 개인키 값
    :return: gncHash
    '''
    owner_address = web3.to_checksum_address(owner_add)
    
    nonce = web3.eth.get_transaction_count(owner_address)

    gas_estimate = mycontract.functions.renounceMinter().estimate_gas({'from': owner_address})
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(web3.to_wei(gas_price, 'gwei'))
    print(f"txfee: {web3.from_wei(gas_estimate * gas_price, 'Ether')}")
    tx = mycontract.functions.renounceMinter().build_transaction(
        {
            'from': owner_add,
            'nonce': nonce,
            'gas': gas_estimate *2,
            "gasPrice": gas_price+ web3.to_wei(2, 'gwei')
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, owner_pv)
    amtTxHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(amtTxHash)
    return gncHash


def ethereum_NFT_change_ownership(web3, mycontract, owner_add , owner_pv, new_owner_add):
    '''
        use             : NFT 컨트랙트의 모든 권한을 위임하는 함수이다 ( 민감한 함수 주의 요함 !!)
        input parameter : 1. web3 : web3 네트워크 연결
                          2. mycontract : abi로 활성화한 컨트랙트 함수들
                          3. pv : 현재 주인의 개인키
                          4. owner : 현재 주인의 주소
                          5. new_owner : 새로운 주인의 주소
        output parameter : gncHash
    '''

    senderAddress = web3.to_checksum_address(owner_add)
    reciverAddress = web3.to_checksum_address(new_owner_add)
    nonce = web3.eth.get_transaction_count(senderAddress)
    gas_price = web3.eth.gas_price
    gas_estimate = mycontract.functions.transferOwnership(reciverAddress).estimate_gas(
        {'from': senderAddress})
    tx = mycontract.functions.transferOwnership(reciverAddress).build_transaction(
        {
            'from': senderAddress,
            'nonce': nonce,
            'gas': gas_estimate * 2,
            'gasPrice':  gas_price+ web3.toWei(2, 'gwei'),
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, owner_pv)
    amtTxHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(amtTxHash)

    return gncHash


##############################################
##### 콜 함수 영역 #####
def ethereum_NFT_totalsuply(web3, mycontract):
    '''
    use              : NFT총 발행량 조회
    input parameter  : 1. web3 : web3 네트워크 연결
                       2. mycontract: abi로 활성화한 컨트랙트 함수들
    output parameter : total_token
     '''
    total_token = mycontract.functions.totalSupply().call()
    print(total_token)
    return total_token


def ethereum_NFT_owner(web3, mycontract, token_id):
    '''
    use              : NFT Token id Owner 주소 조회
    input parameter  : 1. web3 : web3 네트워크 연결
                       2. mycontract : abi로 활성화한 컨트랙트 함수들
                       3. token_id : 조회할 토큰 id
    output parameter : token_owner
    '''
    token_owner = mycontract.functions.ownerOf(token_id).call()
    return token_owner

def ethereum_NFT_uri(web3, mycontract, token_id):
    '''
    use             : NFT Token id uri 조회
    input parameter : 1. web3 : web3 네트워크 연결
                      2. mycontract : abi로 활성화한 컨트랙트 함수들
                      3. token_id : 조회할 토큰 id
    output parameter : tokenid_uri
    '''
    tokenid_uri = mycontract.functions.tokenURI(token_id).call()
    return tokenid_uri


def getbaseuri(web3,mycontract):
     '''
    use             : 현재 컨트랙트에 적용되어 있는 baseuri 확인
    input parameter : 1. web3 : web3 네트워크 연결
                      2. mycontract : abi로 활성화한 컨트랙트 함수들
    output parameter : call_base
    '''
     call_base = mycontract.functions.baseTokenUri().call()
     print(call_base)
     return call_base

def ethereum_erc721a_isminter(web3, mycontract, add):
    '''
    use             : 입력받은 주소가 minter 권한이 있는지 확인용
    input parameter : 1. web3 : web3 네트워크 연결
                      2. mycontract : abi로 활성화한 컨트랙트 함수들
                      3. add : 확인받을 주소값
    output parameter : confirm_role
    '''
    confirm_add = web3.to_checksum_address(add)
    confirm_role = mycontract.functions.isMinter(confirm_add).call()
    print(confirm_role)
    return confirm_role

     
def ethereum_erc721a_walletOfOwner(web3, mycontract, owner_add):
    '''
    use             : 입력받은 주소가 tokenid를 몇개 소유하고 있는지 확인용
    input parameter : 1. web3 : web3 네트워크 연결
                      2. mycontract : abi로 활성화한 컨트랙트 함수들
                      3. owner_add : 확인받을 주소값
    output parameter : owner_token_ls
    '''
    owner_address = web3.to_checksum_address(owner_add)
    owner_token_ls = mycontract.functions.walletOfOwner(owner_address).call()
    print(owner_token_ls)
    return owner_token_ls


##############################################


##### 유틸 함수 영역 ######

def ethereum_NFT_get_image_url(tokenuri):
    

    with urllib.request.urlopen(tokenuri) as url:
        s = url.read()
        sdata = json.loads(s)
        imageurl = sdata['image']

        return imageurl

def ethereum_NFT_snapshot(web3,mycontract):
    '''
    use              : Token id 별 owner와 Token uri를 리스트로 정리
    input parameter  : web3 : web3 네트워크 연결
          mycontract : abi로 활성화한 컨트랙트 함수들
    output parameter : owner_list
    '''
    from web3.middleware import geth_poa_middleware
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    total = ethereum_NFT_totalsuply(web3, mycontract)
    owner_list = []
    for i in range(1, total+1):
        try:
            owner = ethereum_NFT_owner(web3, mycontract, i)
            uri = ethereum_NFT_uri(web3, mycontract, i)
            owner_data = {'TokenId': i, 'Owner': owner, 'URI': uri}
            owner_list.append(owner_data)
        except Exception as e:
            continue
    return owner_list




def ethereum_NFT_result_list(web3, gncHash):

    return {'transactionHash': web3.toHex(gncHash.transactionHash), 'blockNumber': gncHash.blockNumber, 'blockhash': web3.toHex(gncHash.blockHash), 'cumulativeGasUsed': gncHash.cumulativeGasUsed , 'to': gncHash.to }







       






    


