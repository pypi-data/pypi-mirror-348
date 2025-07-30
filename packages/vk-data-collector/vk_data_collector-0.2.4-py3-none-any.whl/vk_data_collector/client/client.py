import requests


class Client:
    base_url = "https://api.vk.com"

    def __init__(self, token: str):
        """
        Initialize VK API client.

        Args:
            token: VK API access token
        """
        self.service_token = token

    def make_request(self, endpoint, params, v="5.199"):
        url = self.base_url + endpoint
        params["access_token"] = self.service_token
        params["v"] = v
        response = requests.get(url, params=params)
        return response
