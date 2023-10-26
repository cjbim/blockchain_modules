from web3 import Web3, HTTPProvider
import json
import datetime
import os
import urllib
import time
import hashlib
import struct
from eth_account.messages import encode_defunct, encode_structured_data, defunct_hash_message


def klaytn_connect_web3(network,Authorization):

    if network == "baobab":

        options ={
            'headers':
                {
                    'Content-Type': 'application/JSON',
                    'Authorization': Authorization,
                    'x-chain-id': '1001'
                }
        }
        web3 = Web3(Web3.HTTPProvider("https://node-api.klaytnapi.com/v1/klaytn",options))

    elif network == "klaytn":
        options ={
            'headers':
                {
                    'Content-Type': 'application/JSON',
                    'Authorization': Authorization,
                    'x-chain-id': '8217'
                }
        }
        web3 = Web3(Web3.HTTPProvider("https://node-api.klaytnapi.com/v1/klaytn",options))

    else :
        print("unknown network error")

    print(web3.is_connected())
    return web3


def klaytn_check_network(web3):
    check = web3.net.version
    if check == "1001":
        network = "baobab"
    elif check == "8217":
        network = "klaytn"
    else:
        network = "unknown"

    return network

def klaytn_klayscope_link(network,contract_address):
    if network == "klaytn":
        uri = f"https://scope.klaytn.com/account/{contract_address}?tabId=txList"
    elif network == "baobab":
        uri = f"https://baobab.scope.klaytn.com/account/{contract_address}?tabId=txList"
    else:
        uri = "unknown"
    return uri
    
def klaytn_getBalance(web3, account):
	account = web3.to_checksum_address(account)
	balance = web3.from_wei(web3.eth.get_balance(account), 'ether')
	return balance

def klaytn_read_abi(file_name):
	with open(file_name) as f:
		info_json = json.load(f)
	return info_json["abi"]

def klaytn_getContract(web3, contractAddress, contractAbi):
	file = open(contractAbi, 'r', encoding='utf-8')
	contractaddress = web3.to_checksum_address(contractAddress)
	mycontract = web3.eth.contract(abi=file.read(), address=contractaddress)
	return mycontract


def klaytn_erc20_token_balance(web3, mycontract, useraddress):  # coin 소유량 조회
    token_balance = mycontract.functions.balanceOf(useraddress).call()
    return token_balance


def klaytn_erc20_token_totalsuply(web3, mycontract):
    '''
    use              : Token총 발행량 조회
    input parameter  : 1. web3 : web3 네트워크 연결
                       2. mycontract: abi로 활성화한 컨트랙트 함수들
    output parameter : total_token
     '''

    total_token = mycontract.functions.totalSupply().call()
    print(total_token)
    return total_token

def klaytn_erc20_token_approve(web3,mycontract, sender, sender_pv, spender, value):
    owner_add = web3.to_checksum_address(sender)
    spender = web3.to_checksum_address(spender)
    nonce = web3.eth.get_transaction_count(owner_add)
    gas_estimate = mycontract.functions.approve(spender,value).estimate_gas({'from': owner_add})
    lst = []
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(gas_price)
    before_tx_fee = web3.from_wei(gas_estimate * gas_price, 'Ether')
    lst.append(before_tx_fee)
    print(before_tx_fee)
    tx = mycontract.functions.approve(spender,value).build_transaction(
        {
            'from': owner_add,
            'nonce': nonce,
            "gasPrice": gas_price
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, sender_pv)
    amtTxHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(amtTxHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)
    if before_tx_fee == after_tx_fee:
        lst.append('true')
    else:
        lst.append('false')
    return lst, gncHash


def klaytn_erc20_token_mint(web3,mycontract, sender, sender_pv, value):
    owner_add = web3.to_checksum_address(sender)
    nonce = web3.eth.get_transaction_count(owner_add)
    gas_estimate = mycontract.functions.mint(owner_add,value).estimate_gas({'from': owner_add})
    lst = []
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(gas_price)
    before_tx_fee = web3.from_wei(gas_estimate * gas_price, 'Ether')
    lst.append(before_tx_fee)
    print(before_tx_fee)
    tx = mycontract.functions.mint(owner_add,value).build_transaction(
        {
            'from': owner_add,
            'nonce': nonce,
            "gasPrice": gas_price
        }
    )
    print(tx)
    signed_txn = web3.eth.account.sign_transaction(tx, sender_pv)
    amtTxHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(amtTxHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)
    if before_tx_fee == after_tx_fee:
        lst.append('true')
    else:
        lst.append('false')
    return lst, gncHash

def klaytn_erc20_token_burning(web3,mycontract, sender, sender_pv, value):
    owner_add = web3.to_checksum_address(sender)
    nonce = web3.eth.get_transaction_count(owner_add)
    gas_estimate = mycontract.functions.burning(value).estimate_gas({'from': owner_add})
    lst = []
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(gas_price)
    before_tx_fee = web3.from_wei(gas_estimate * gas_price, 'Ether')
    lst.append(before_tx_fee)
    print(before_tx_fee)
    tx = mycontract.functions.burning(value).build_transaction(
        {
            'from': owner_add,
            'nonce': nonce,
            "gasPrice": gas_price
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, sender_pv)
    amtTxHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(amtTxHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)
    if before_tx_fee == after_tx_fee:
        lst.append('true')
    else:
        lst.append('false')
    return lst, gncHash

def klaytn_verify_allowance(web3,mycontract,owner,spender):
     verify = mycontract.functions.allowance(owner,spender).call()
     print(verify)

def klaytn_permit_hash(web3, mycontract,token_add, sender_add, sender_pk, spender_add,deadline, amount):
    sender = web3.to_checksum_address(sender_add)
    spender =  web3.to_checksum_address(spender_add)
    nonce = mycontract.functions.nonces(sender_add).call()
    contract_name = mycontract.functions.name().call()
    msg ={
    "domain": {
        "name": contract_name,
        "version": "1",
        "chainId": int(web3.net.version),
        "verifyingContract": token_add
    },
    "message": {
        "owner": sender,
        "spender": spender,
        "value": amount,
        "nonce": int(nonce),
        "deadline": deadline
    },
    "primaryType": "Permit",
    "types": {
        "EIP712Domain": [
        {
            "name": "name",
            "type": "string"
        },
        {
            "name": "version",
            "type": "string"
        },
        {
            "name": "chainId",
            "type": "uint256"
        },
        {
            "name": "verifyingContract",
            "type": "address"
        }
        ],
        "Permit": [
        {
            "name": "owner",
            "type": "address"
        },
        {
            "name": "spender",
            "type": "address"
        },
        {
            "name": "value",
            "type": "uint256"
        },
        {
            "name": "nonce",
            "type": "uint256"
        },
        {
            "name": "deadline",
            "type": "uint256"
        }
        ]
    }
    }
    new_msg = json.loads(json.dumps(msg))
    new_msg['domain']['version'] = str(new_msg['domain']['version'])
    encoded_data=encode_structured_data(new_msg)
    print(encoded_data)
    owner_pk = web3.eth.account.from_key(sender_pk)
    signature = owner_pk.sign_message(encoded_data)
    print(signature)
    v = int(signature.v)
    r = to_32byte_hex(signature.r)
    s = to_32byte_hex(signature.s)
    confirm = web3.eth.account.recover_message(encoded_data ,signature = signature.signature)
    print(confirm)
    return v,r,s
def to_32byte_hex(val):
  return Web3.to_hex(Web3.to_bytes(val).rjust(32, b'\0'))



def klaytn_metatran(web3, mycontract, token_add, spender, spender_pk, sender, sender_pk, reciepter, amt, fee, deadline):
    spender = web3.to_checksum_address(spender)
    nonce = web3.eth.get_transaction_count(spender)
    v,r,s = ether_permit_hash(web3, mycontract,token_add, sender, sender_pk, spender,deadline, amt+fee)
    gas_estimate = mycontract.functions.transferWithPermit(sender, spender, reciepter, amt,fee,deadline, v,r,s).estimate_gas({'from': spender})
    lst = []
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(gas_price)
    before_tx_fee = web3.from_wei(gas_estimate * gas_price, 'Ether')
    lst.append(before_tx_fee)
    print(before_tx_fee)
    tx = mycontract.functions.transferWithPermit(sender, spender, reciepter, amt,fee,deadline, v,r,s).build_transaction(
        {
            'from': spender,
            'nonce': nonce,
            "gasPrice": gas_price
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, spender_pk)
    amtTxHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(amtTxHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)
    if before_tx_fee == after_tx_fee:
        lst.append('true')
    else:
        lst.append('false')
    return lst, gncHash
