
from web3 import Web3
import Polygon_utill
"""
polygon metic transfer

"""




def polygon_metic_transfer(web3,sender,sender_pk,reciever,amt,gas_price):
    web3.toChecksumAddress(sender)
    web3.toChecksumAddress(reciever)
    nonce = web3.eth.get_transaction_count(sender)
    gas_estimate = web3.eth.estimateGas({'from': sender, 'to': reciever, 'value': web3.toWei(amt, "ether")})
    #print(gas_estimate)
    tx = {
            'nonce': nonce,
            'to': reciever,
            'value': web3.toWei(amt, 'ether'),
            'gas': gas_estimate,
            "gasPrice": web3.toWei(gas_price , 'gwei'),
            "chainId": 80001
        }
    sign_tx = web3.eth.account.signTransaction(tx,sender_pk)
    tx_hash = web3.eth.sendRawTransaction(sign_tx.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(tx_hash)
    return gncHash


if __name__ == "__main__":
    


