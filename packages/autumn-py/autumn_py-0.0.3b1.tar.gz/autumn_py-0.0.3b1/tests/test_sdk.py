from src.autumn.sdk import *
from src.autumn.client import Autumn


def test_sdk():
    print()

    print("Hello World")
    sdkOne()
    sdkTwo()
    autumn = Autumn(
        secret_key="am_sk_test_rR8wb9FuPXNFmQRo3PalS2XqF6XNA1k5gb9inFzABW")

    result = autumn.attach(
        params={
            "customer_id": "1234567890",
            "product_id": "1234567890",
            "entity_id": "1234567890",
        })
    print("Result: ", result)
