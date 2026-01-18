from web3 import Web3
from django.conf import settings

w3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))

ADMIN_PRIVATE_KEY = settings.ADMIN_PRIVATE_KEY
ADMIN_ADDRESS = settings.ADMIN_WALLET_ADDRESS


def send_fake_eth(to_address, amount_eth=0.01):
  try:
     w3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))

     if not w3.is_connected():
            print("⚠️ Ganache not connected")
            return None
  except Exception as e:
        print("⚠️ Ganache connection error:", e)


  try:
    nonce = w3.eth.get_transaction_count(ADMIN_ADDRESS)
  
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': w3.to_wei(amount_eth, 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei('20', 'gwei')
    }

    signed_tx = w3.eth.account.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return tx_hash.hex()
  except Exception as e:
        print("⚠️ Blockchain error:", e)
        return None