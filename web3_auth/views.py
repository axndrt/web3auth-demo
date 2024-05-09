"""
Web3 Auth ViewSet
~~~~~~~~~~~~~~~~~

This module contains a Django Rest Framework viewset for Web3 authentication.

The viewset provides endpoints for generating and verifying Web3 signatures.

Endpoints:
    - generate: Generates a message for a given Ethereum address and stores it in Redis.
    - verify: Verifies a Web3 signature against the stored message in Redis and returns an access token.

Classes:
    Web3AuthViewSet: A DRF viewset for Web3 authentication.

"""

from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from web3_auth.redis import RedisClient
from web3_auth.utils import generate_message, recover_address
from web3_auth.validators import validate_eth_address

User = get_user_model()
redis_client = RedisClient()


class Web3AuthViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=["POST"])
    def generate(self, request):
        address = request.data.get("address", "").lower()
        if not validate_eth_address(address):
            return Response(
                status=400, data={"error": "Address must be Ethereum format"}
            )
        message = generate_message(address)
        redis_client.set_with_global_ttl(address, message)
        return Response({"message": message})

    @action(detail=False, methods=["POST"])
    def verify(self, request):
        address = request.data.get("address", "").lower()
        if not validate_eth_address(address):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Address must be Ethereum format"},
            )
        signature = request.data.get("signature", "")
        message = redis_client.get_by_key(address)
        if message is None:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"error": "Unauthorized request"},
            )

        if address != recover_address(message, signature):
            return Response(
                status=status.HTTP_401_UNAUTHORIZED, data={"error": "Bad signature"}
            )
        redis_client.delete_by_key(address)
        user, _ = User.objects.get_or_create(username=address)
        jwt = AccessToken.for_user(user)
        return Response(status=status.HTTP_200_OK, data={"access_token": str(jwt)})
