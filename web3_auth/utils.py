import uuid

from eth_account.messages import encode_defunct
from web3 import Web3


def recover_address(message, signature):
    web3_client = Web3(Web3.HTTPProvider(""))
    message = message.decode("UTF-8")
    address = web3_client.eth.account.recover_message(
        encode_defunct(text=message), signature=signature
    )
    return address.lower()


def generate_message(address):
    nonce = str(uuid.uuid4())
    message = f"Welcome to our Platform Nonce {nonce} Account {address}"
    return message
