from tronpy import Tron
from tronpy.keys import PrivateKey
import json
import requests

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

def tron_token_get_contract(client,contract_add):
    '''
    :use : trc-20 토큰의 abi 정보를 네트워크에서 가져온다
    :param client: 트론 네트워크
    :param contract_add: 배포한 컨트랙트 주소
    :return: mycontract
    '''
    mycontract = client.get_contract(contract_add)
    return mycontract


def tron_token_totalsupply(client,mycontract):
    '''
    :use : Token총 발행량 조회
    :param client: tron 네트워크 연결
    :param mycontract: abi로 활성화한 컨트랙트 함수들
    :return: total_token
    '''

    total_token = mycontract.functions.totalSupply()
    print(total_token)
    return total_token



def tron_token_transfer(client,mycontract,sender_address, sender_pk, receiver_address,amt):
    '''
    :use : TRC-20 토큰을 보낸다
    :param client: 트론 네트워크 연결
    :param mycontract: abi로 활성화한 컨트랙트 함수들
    :param sender_address: 보내는 사람의 주소
    :param sender_pk: 보내는 사람의 개인키
    :param receiver_address: 받는 사람의 주소
    :param amt: 보내는 양
    :return: reciept
    '''

    privatekey=PrivateKey(bytes.fromhex(sender_pk))
    Amy = amt*1000000000000000000

    tx = (
        mycontract.functions.transfer(receiver_address, Amy)
        .with_owner(sender_address)
        .fee_limit(10_000_000)
        .build()
        .sign(privatekey)
    )
    tx_id = tx.txid
    print("tx_id: ", tx_id)
    reciept = tx.broadcast().wait


    return reciept

def tron_token_get_balance(client, mycontract, user_add):
    '''
    :use : trc-20 토큰의 수량을 조회 한다.
    :param client: 트론 네트워크 연결
    :param mycontract: abi로 활성화한 컨트랙트 함수들
    :param user_add: 조회 할 유저의 주소
    :return: balance
    '''
    balance = mycontract.functions.balanceOf(user_add)
    print(balance)
    return balance
def tron_token_mint(client,mycontract,owner,owner_pv,amt):
    Amy = amt * 1000000000000000000
    tx = (
        mycontract.functions.mint(owner, amt)
        .with_owner(owner)
        .fee_limit(10_000_000)
        .build()
        .sign(owner_pv)
    )
    tx_id = tx.txid
    print("tx_id: ", tx_id)
    reciept = tx.broadcast().wait

def get_events(API_URL_BASE, contract_add, timestamp=None, page = None ):
    '''
    :use : 컨트랙트의 전체 거래 기록을 가져온다
    :param API_URL_BASE: 트론 API 네트워크 연결
    :param contract_add: 조회할 컨트랙트 주소
    :param timestamp: 데이터의 타임 스탬프를 넣으면 타임스탬프 기준으로 그시간 이후의 데이터를 가져온다.
    :param page: 가져올 수 있는 데이터의 갯수는 200개가 한계 이므로 200개가 넘어가면 페이지를 넘어가면 된다.
    :return: tx_json
    '''

    if timestamp is not None:
        url = f"{API_URL_BASE}v1/contracts/{contract_add}/events?min_block_timestamp={timestamp}&limit=200"
    elif page is not None:
        url = f"{API_URL_BASE}v1/contracts/{contract_add}/events?limit=200&fingerprint={page}"
    elif timestamp is not None and page is not None :
        url = f"{API_URL_BASE}v1/contracts/{contract_add}/events?min_block_timestamp={timestamp}&limit=200&fingerprint={page}"
    else:
        url = f"{API_URL_BASE}v1/contracts/{contract_add}/events?limit=200"


    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    tx = response.text
    tx_json = json.loads(tx)
    print(tx_json)
    return tx_json

def get_last_timestamp(API_URL_BASE,contract_add):
    '''
    :use : 마지막 데이터의 timestamp를 가져온다.
    :param API_URL_BASE: 트론 API 네트워크 연결
    :param contract_add: 컨트랙트 주소
    :return: tx_data
    '''
    url = f"{API_URL_BASE}v1/contracts/{contract_add}/events?limit=200"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    tx = response.text
    tx_json = json.loads(tx)
    tx_data = tx_json["data"][0]["block_timestamp"]
    print(tx_data)
    return tx_data


def get_first_timestamp(API_URL_BASE,contract_add):
    '''
    :use : 첫 거래기록의 timestamp를 가져온다.
    :param API_URL_BASE: 트론 API 네트워크 연결
    :param contract_add: 컨트랙트 주소
    :return: tx_data
    '''
    url = f"{API_URL_BASE}v1/contracts/{contract_add}/events?limit=200"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    tx = response.text
    tx_json = json.loads(tx)
    tx_data = tx_json["data"][-1]["block_timestamp"]
    print(tx_data)
    return tx_data




'''
def get_contract_firstblcok(API_URL_BASE,contract_add):
    url = f"{API_URL_BASE}v1/contracts/{contract_add}/events?limit=200"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    tx = response.text
    tx_json = json.loads(tx)
    tx_data = tx_json["data"][-1]["block_number"]
    print(tx_data)
    return tx_data

def get_contract_lastblcok(API_URL_BASE,contract_add):
    url = f"{API_URL_BASE}v1/contracts/{contract_add}/events?limit=200"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    tx = response.text
    tx_json = json.loads(tx)
    tx_data = tx_json["data"][0]["block_number"]
    print(tx_data)
    return tx_data


def get_all_lastblock(API_URL_BASE):
    url = f"{API_URL_BASE}v1/blocks/latest/events"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    tx = response.text
    tx_json = json.loads(tx)
    tx_data = tx_json["data"][0]["block_number"]
    print(tx_data)
    return tx_data


def get_events_blocknum(API_URL_BASE,contract_add,blcoknum):
    url = f"{API_URL_BASE}v1/contracts/{contract_add}/events?block_number={blcoknum}&limit=200"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    tx = response.text
    tx_json = json.loads(tx)

    print(tx_json)
    return tx_json

def search_tx_in_the_blcok(API_URL_BASE,contract_add):
   
    first_blcok = get_contract_firstblcok(API_URL_BASE,contract_add)
    latest_blcok = get_all_lastblock(API_URL_BASE)
    search_unit = latest_blcok - first_blcok
    tx_data = []
    for i in range(first_blcok, latest_blcok):
        tx = get_events_blocknum(API_URL_BASE, contract_add, i)
        if tx["data"] == [] :
            print("none")
        else:
            tx_data.append(tx)
    print(tx_data)


너무 느리다. 효율 떨어짐
'''






if __name__ == "__main__":
    
