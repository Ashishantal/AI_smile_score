import uuid
from decimal import Decimal
from django.conf import settings

def send_fake_eth(wallet_address):
    """
    DEMO MODE:
    No real blockchain interaction
    Generates fake tx hash
    """
    fake_tx_hash = "0x" + uuid.uuid4().hex
    return fake_tx_hash, settings.DEMO_REWARD_ETH
