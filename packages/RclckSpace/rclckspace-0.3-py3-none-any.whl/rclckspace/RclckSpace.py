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
        
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(response.text)