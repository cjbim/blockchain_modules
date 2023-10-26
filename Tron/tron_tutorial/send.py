from tronpy import Tron
from tronpy.keys import PrivateKey

def send(sender_address, sender_pk, send_trx, receiver_address):
    client=Tron(network='shasta')
    try:
        privatekey=PrivateKey(bytes.fromhex(sender_pk))

        txn=client.trx.transfer(sender_address, receiver_address, send_trx*1000000)\
            .memo("Test Sending Tron").build().inspect().sign(privatekey).broadcast()

        return txn.wait()

    except Exception as ex:
        return ex

