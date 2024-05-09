from django.urls import path

from web3_auth.views import Web3AuthViewSet

urlpatterns = [
    path(
        "generate/",
        Web3AuthViewSet.as_view({"post": "generate"}),
        name="web3-auth-generate",
    ),
    path(
        "verify/", Web3AuthViewSet.as_view({"post": "verify"}), name="web3-auth-verify"
    ),
]
