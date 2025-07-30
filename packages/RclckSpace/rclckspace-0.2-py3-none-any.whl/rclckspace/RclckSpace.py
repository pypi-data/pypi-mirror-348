import requests

class RclckSpace:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://rclck.space/api.php"

    def create_short_url(self, long_url: str) -> str:
        data = {
            "api_key": self.api_key,
            "url": long_url
        }
        response = requests.post(self.api_url, json=data)
        return response.text 