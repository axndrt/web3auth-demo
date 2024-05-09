from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from web3_auth.redis import RedisClient
from web3_auth.utils import generate_message, recover_address
from web3_auth.validators import validate_eth_address

User = get_user_model()


class Web3AuthViewSet(viewsets.GenericViewSet):

    redis_client = RedisClient()

    @action(detail=False, methods=["POST"])
    def generate(self, request):
        address = request.data.get("address", "").lower()
        if not validate_eth_address(address):
            return Response(
                status=400, data={"error": "Address must be Ethereum format"}
            )
        message = generate_message(address)
        self.redis_client.set_with_global_ttl(address, message)
        return Response({"message": message})

    @action(detail=False, methods=["POST"])
    def verify(self, request):
        address = request.data.get("address", "").lower()
        if not validate_eth_address(address):
            return Response(
                status=400, data={"error": "Address must be Ethereum format"}
            )
        signature = request.data.get("signature", "")
        message = self.redis_client.get_by_key(address)
        if message is None:
            return Response(status=401, data={"error": "Unauthorized request"})

        if address != recover_address(message, signature):
            return Response(status=401, data={"error": "Bad signature"})
        self.redis_client.delete_by_key(address)
        (user, _) = User.objects.get_or_create(username=address)
        jwt = AccessToken.for_user(user)
        return Response(status=200, data={"access_token": str(jwt)})
