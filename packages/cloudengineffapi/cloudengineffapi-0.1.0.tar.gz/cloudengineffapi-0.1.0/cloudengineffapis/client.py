import requests
from collections import deque
import time

# Rate limit decorator to enforce N requests per T seconds
def rate_limit(N, T):
    timestamps = deque(maxlen=N)
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.time()
            if len(timestamps) == N:
                oldest = timestamps[0]
                if now - oldest < T:
                    wait_time = T - (now - oldest)
                    time.sleep(wait_time)
            result = func(*args, **kwargs)
            timestamps.append(time.time())
            return result
        return wrapper
    return decorator

# Client class to interact with APIs
class CloudEngineClient:
    def __init__(self, api_key="khalid"):  # Hardcoded API key for simplicity
        self.api_key = api_key

    @rate_limit(10, 3600)  # 10 requests per hour
    def get_likes(self, region, uid):
        url = f"https://likes.api.v2.cloudenginexe.com/cloudlike?region={region}&uid={uid}&api_key={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @rate_limit(100, 60)  # 100 requests per minute
    def get_info(self, region, uid):
        url = f"https://info.api.cloudenginexe.com/api/info?api_key={self.api_key}&region={region}&uid={uid}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @rate_limit(1000, 60)  # 1000 requests per minute
    def check_ban(self, uid):
        url = f"https://bancheck.cloudenginecore.com/api/bancheck/{uid}?api_key={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()