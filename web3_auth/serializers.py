from rest_framework import serializers

from web3_auth.validators import validate_eth_address


class Web3AuthSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=42)
    signature = serializers.CharField()

    def validate_address(self, value):
        """Validate that the address is in Ethereum format."""
        value = value.lower()
        if not validate_eth_address(value):
            raise serializers.ValidationError("Address must be Ethereum format")
        return value
