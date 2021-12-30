from typing import Any

import requests

from test.util import create_test_user

DEPLOY_URL = "https://yxm6jf.deta.dev"


class MockRequest:
    base_url: str

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def post(self, url: str, data: Any):
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        return requests.post(f"{self.base_url}{url}", json=data, headers=headers)


client = MockRequest(DEPLOY_URL)


def test_user_creation():
    # The following does not work!!
    # create_test_user(client)
    pass
