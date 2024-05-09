from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from web3_auth.redis import redis_client
from web3_auth.serializers import Web3GenerateSerializer, Web3VerifySerializer
from web3_auth.utils import generate_message, recover_address

User = get_user_model()


class Web3AuthViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=["POST"])
    def generate(self, request):
        serializer = Web3GenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.validated_data["address"]
        message = generate_message(address)
        redis_client.set_with_global_ttl(address, message)
        return Response({"message": message})

    @action(detail=False, methods=["POST"])
    def verify(self, request):
        serializer = Web3VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        signature = serializer.validated_data["signature"]
        address = serializer.validated_data["address"]
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
