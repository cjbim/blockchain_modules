from tronpy import Tron

def account_balance(address):
    client=Tron(network='shasta')
    balance=client.get_account_balance(address)
    print(balance)


#address='THFcSMyMaeBqeSUp8vKMZ8NKNbWUwxVbHx'
address='TFmTt6p43KC8NbuVfkwPzwNhU1ee3WWb8H'
account_balance(address)