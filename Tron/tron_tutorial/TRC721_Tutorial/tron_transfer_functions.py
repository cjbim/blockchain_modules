from tronpy import Tron
from tronpy.keys import PrivateKey
'''
date = 2022-10-27

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


def create_wallet(client):
    '''
    :use : 지갑 생성
    :param client: 지갑을 만들 트론 네트워크
    :return:
    '''
    address=client.generate_address()
    print("Wallet address: %s" %address['base58check_address'])
    print("Private Key: %s" %address['private_key'])

def account_balance(client, address):
    '''
    :use : 지갑에 있는 트론 잔액 출력
    :param client: 트론 네트워크
    :param address: 확인할 지갑 주소
    :return: balance
    '''
    balance=client.get_account_balance(address)
    print(balance)
    return balance


def send(client,sender_address, sender_pk, send_trx, receiver_address,memo):
    '''
    :use : 트론 전송
    :param client: 트론 네트워크
    :param sender_address: 보내는 사람 주소
    :param sender_pk: 보내는 사람 개인키 주소
    :param send_trx: 보낼 트론의 양
    :param receiver_address: 받는 사람 주소
    :param memo: 보내면서 보낼 내용
    :return:
    '''
    try:
        privatekey=PrivateKey(bytes.fromhex(sender_pk))
        amt = send_trx*1000000

        txn=client.trx.transfer(sender_address, receiver_address, amt)\
            .memo(memo).build().inspect().sign(privatekey).broadcast()

        return txn.wait()

    except Exception as ex:
        return ex


if __name__ == "__main__":
