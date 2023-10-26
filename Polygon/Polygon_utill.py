from web3 import Web3, HTTPProvider
import json
import requests
import os
"""
polygon

"""


def polygon_connectWeb3(connect_host=None): #web3 connect rpcuri 선택
    if connect_host is None:
        infura_url = "http://localhost:8545"
    elif connect_host == "mumbai":
        infura_url = "https://polygon-testnet-rpc.allthatnode.com:8545"
    elif connect_host == "polygon":
        infura_url = "https://polygon-mainnet-rpc.allthatnode.com:8545"
    else:
        infura_url = "http://localhost:8545"
    web3 = Web3(Web3.HTTPProvider(infura_url))
    print(f"{infura_url} connect is {web3.is_connected()}")
    return web3


def polygon_gasPrice(priceType):


	req = requests.get('https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=94GX5S8H6QIJVC2R9MX33V8AXMHC55DMXN')
	res = json.loads(req.content)
	if priceType == "average":
		return res['result']['ProposeGasPrice']
	elif priceType == "safelow":
		return res['result']['SafeGasPrice']
	elif priceType == "fast":
		return res['result']['FastGasPrice']
	elif priceType == "low":
		return res['result']['suggestBaseFee']
	else:
	    return res['result']['average']


def polygon_contract_abi(web3, contractAddress, abi):
    '''
    use              : 컨트랙트 주소와 abi를 통해 스마트 컨트랙트 함수를 사용하기위해 연결
    input parameter  : 1. web3 : web3 네트워크 연결
                       2. contractAddress: 컨트랙트 주소
                       3. abi: abi 경로
    output parameter : mycontract
    '''
    file = open(abi, 'r', encoding='utf-8')
    contractaddress = web3.to_checksum_address(contractAddress)
    mycontract = web3.eth.contract(abi=file.read(), address=contractaddress)
    return mycontract
