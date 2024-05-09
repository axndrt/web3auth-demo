from eth_utils import is_hex_address
from rest_framework import serializers


class Web3AuthSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=42)
    signature = serializers.CharField()

    def validate_address(self, value):
        """Validate that the address is in Ethereum format."""
        value = value.lower()
        if not self.validate_eth_address(value):
            raise serializers.ValidationError("Address must be Ethereum format")
        return value

    @staticmethod
    def validate_eth_address(value):
        return is_hex_address(value)
