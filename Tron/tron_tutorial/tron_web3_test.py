import tronpy
from tronpy import Tron
from tronpy.keys import PrivateKey
import json
import requests
import collections
import statistics
import sys
import base58
'''
date : 2022-10-27
'''

def tron_connect_network(connect_host=None):
    '''
        :use : 트론 네트워크 연결
        :param connect_host: 네트 워크 이름
        :return: client
    '''


    if connect_host is None:

        net_work = "shasta"
        client = Tron(network=net_work)
    elif connect_host == "shasta":
        net_work = "shasta"
        client = Tron(network=net_work)
    elif connect_host == "mainnet":
        client = Tron()
    elif connect_host == "nile":
        client = Tron(network="nile")
    else:
        net_work = "shasta"
        client = Tron(network=net_work)
    return client



def tron_get_apiurl(connect_host=None):
    '''.
    :use : 거래 내역이나 기록을 가져오기위한 JRPC 주소를 가져온다
    :param connect_host: 트론 네트워크
    :return: API_URL_BASE
    '''

    if connect_host is None:
        API_URL_BASE = 'https://api.shasta.trongrid.io/'
    elif connect_host == "shasta":
        API_URL_BASE = 'https://api.shasta.trongrid.io/'
    elif connect_host == "mainnet":
        API_URL_BASE = 'https://api.trongrid.io/'
    elif connect_host == "nile":
        API_URL_BASE = 'https://nile.trongrid.io/'
    else:
        API_URL_BASE = 'https://api.shasta.trongrid.io/'
    return API_URL_BASE


def tron_get_getGasprice(api_url):


    energy_price = f"{api_url}wallet/getenergyprices"
    headers = {"accept": "application/json"}

    response = requests.post(energy_price, headers=headers)
    ls = response.json()
    print(ls['prices'])

def tron_account_balance(client, address):
    balance=client.get_account_balance(address)
    print(balance)
    return balance

def tron_create_wallet(client):
    address=client.generate_address()
    print("Wallet address: %s" %address['base58check_address'])
    print("Private Key: %s" %address['private_key'])

def tron_get_account_resource(client, address):
    resource = client.get_account_resource(address)
    print(f"에너지 한도: {resource['EnergyLimit']}")
    print(f"자산 동결로 얻은 대역폭 :{resource['NetLimit']}")
    print(f"총 대역폭 한도: {resource['freeNetLimit'] + resource['NetLimit']}")
    if ('freeNetUsed', 'NetUsed',) in resource:
        use_net = (resource['freeNetLimit'] - resource['freeNetUsed']) + (resource['NetLimit'] - resource['NetUsed'])
    else:
        use_net = (resource['freeNetLimit']) + (resource['NetLimit'] )
    print(f"사용 가능한 대역폭: {use_net}")
    if 'EnergyUsed' in resource:
        energy_use = resource['EnergyLimit'] - resource['EnergyUsed']
    else:
        energy_use = resource['EnergyLimit']
    print(f"사용 가능한 에너지: {energy_use}")

def tron_get_account_info(client, address):
    info = client.get_account(address)
    balance = info['balance']/1000000
    print(f"사용가능 금액: {balance} TRX")
    energy_frozen = info['account_resource']['frozen_balance_for_energy']['frozen_balance']/1000000
    print(f"에너지 스테이킹 동결 금액: {energy_frozen} TRX")
    bandwidth_frozen = info['frozen'][0]['frozen_balance']/1000000
    print(f"대역폭 스테이킹 동결 금액: {bandwidth_frozen} TRX")
    total_balance = balance + energy_frozen + bandwidth_frozen
    print(f"총금액: {total_balance} TRX")



def tron_send(client, sender_address, sender_pk, send_trx, receiver_address):
    try:
        privatekey=PrivateKey(bytes.fromhex(sender_pk))

        txn=client.trx.transfer(sender_address, receiver_address, send_trx*1000000)\
            .memo("Test Sending Tron").build().inspect().sign(privatekey).broadcast()

        return txn.wait()

    except Exception as ex:
        return ex
def tron_contract_abi(web3,contractAddress,abi): #컨트랙트 abi 연결
    file = open(abi, 'r', encoding='utf-8')
    mycontract = web3.eth.contract(abi=file.read(), address=contractAddress)
    return mycontract



if __name__ == "__main__":
 
