from tronpy import Tron

def create_wallet():
    client=Tron(network='shasta')
    address=client.generate_address()
    print("Wallet address: %s" %address['base58check_address'])
    print("Private Key: %s" %address['private_key'])


create_wallet()