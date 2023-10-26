from tronpy import Tron
from tronpy.keys import PrivateKey
client=Tron(network='nile')


def mint(mintAddress, owner_pk, token_contract, tokenURI, num):
    contract = client.get_contract(token_contract)
    priv_key = PrivateKey(bytes.fromhex(owner_pk))
    idx = contract.functions.totalSupply()

    for i in range(idx+1,idx+1+num):
        txn=(
            contract.functions.mintWithTokenURI(mintAddress, i, tokenURI+str(i)+".json")
            .with_owner(mintAddress)
            .fee_limit(100000000)
            .build()
            .sign(priv_key)
        )

        print(txn.broadcast().wait())




