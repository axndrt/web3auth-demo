import uuid

from eth_account.messages import encode_defunct
from web3 import Web3


def recover_address(message, signature):
    web3_client = Web3(Web3.HTTPProvider(""))
    message = message.decode()
    address = web3_client.eth.account.recover_message(
        encode_defunct(text=message), signature=signature
    )
    return address.lower()


def generate_message(address):
    return f"Welcome to our Platform Nonce {uuid.uuid4()} Account {address}"
