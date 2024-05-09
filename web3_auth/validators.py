from eth_utils import is_hex_address


def validate_eth_address(value):
    return is_hex_address(value)
