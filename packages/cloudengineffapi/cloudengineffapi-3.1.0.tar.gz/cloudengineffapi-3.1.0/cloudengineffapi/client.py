import requests
import threading
import time
from collections import deque
from typing import Dict, Any

def rate_limit(N: int, T: float):
    """Decorator to enforce rate limits of N requests per T seconds in a thread-safe manner."""
    timestamps = deque(maxlen=N)
    lock = threading.Lock()
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                with lock:
                    now = time.time()
                    while timestamps and now - timestamps[0] >= T:
                        timestamps.popleft()
                    if len(timestamps) < N:
                        timestamps.append(now)
                        break
                    else:
                        wait_time = T - (now - timestamps[0])
                time.sleep(wait_time)
            return func(*args, **kwargs)
        return wrapper
    return decorator

class CloudEngineClient:
    """Advanced client for interacting with CloudEngineFF APIs."""
    
    def __init__(self, api_key: str = "khalid"):
        """Initialize the client with an internal API key and a session for efficient requests."""
        self.api_key = api_key
        self.session = requests.Session()
    
    @rate_limit(10, 21600)  # 10 requests per 6 hours
    def get_likes(self, region: str, uid: str) -> Dict[str, Any]:
        """Fetch likes for a user in a specific region."""
        url = f"https://likes.api.v2.cloudenginexe.com/cloudlike?region={region}&uid={uid}&api_key={self.api_key}"
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    @rate_limit(100, 60)  # 100 requests per minute
    def get_info(self, region: str, uid: str) -> Dict[str, Any]:
        """Fetch information for a user in a specific region."""
        url = f"https://info.api.cloudenginexe.com/api/info?api_key={self.api_key}&region={region}&uid={uid}"
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    @rate_limit(1000, 60)  # 1000 requests per minute
    def check_ban(self, uid: str) -> Dict[str, Any]:
        """Check if a user is banned."""
        url = f"https://bancheck.cloudenginecore.com/api/bancheck/{uid}?api_key={self.api_key}"
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    @rate_limit(50, 60)  # Hypothetical limit: 50 requests per minute
    def get_status(self, uid: str) -> Dict[str, Any]:
        """Fetch the status of a user (e.g., active/inactive)."""
        url = f"https://status.api.cloudenginexe.com/api/status?uid={uid}&api_key={self.api_key}"
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Close the session to free up resources."""
        self.session.close()