# flip_qwen_backend/client.py

import requests

class BackendServiceClient:
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')

    def get_server_pool(self) -> dict:
        url = f"{self.server_url}/server_pool"
        try:
            res = requests.get(url, timeout=5)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed: {e}")