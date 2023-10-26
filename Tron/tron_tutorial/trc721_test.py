from tronpy import Tron, Contract
from tronpy.keys import PrivateKey
import solcx
import json
solcx.install_solc('0.5.8')


def tron_connect_network(connect_host=None):


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


def trc721_deploy(client, file_path, sender_address, sender_pk, name, symbol):
    priv_key = PrivateKey(bytes.fromhex(sender_pk))
    res = solcx.compile_files(
        [file_path],
        output_values=["abi", "bin"],
        solc_version="0.5.8"
    )
    print('a')
    abi = res[file_path + ':trc721']['abi']
    with open('contractabi', 'w') as f:
        json.dump(abi, f)
    bytecode = res[file_path + ':trc721']['bin']
    with open('bincode', 'w') as f:
        json.dump(bytecode, f)
    mycontract = Contract(bytecode=bytecode, abi=abi)
    #tx = mycontract.constructor(name, symbol)
    print(mycontract)
    exit()


    txn = (
        client.trx.deploy_contract(sender_address, tx)
        .fee_limit(5_000_000)
        .build()
        .sign(priv_key)
    )
    print(txn)
    result = txn.broadcast().wait()
    print(result)
    print('Created:', result['contract_address'])

    created_cntr = client.get_contract(result['contract_address'])


if __name__ == "__main__":
 
