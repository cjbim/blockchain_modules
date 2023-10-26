from tronpy import Tron
from tronpy.keys import PrivateKey

def token_send(sender, sender_pk, receiver, token_contract, tokenID):
    client=Tron(network='nile')
    priv_key=PrivateKey(bytes.fromhex(sender_pk))
    contract=client.get_contract(token_contract)

    txn=(
        contract.functions.transferFrom(sender, receiver, tokenID)
        .with_owner(sender)
        .fee_limit(100000000)
        .build()
        .sign(priv_key)
    )

    print(txn.broadcast().wait())


