import requests
from collections import deque
import time
import random

class CloudEngineClient:
    def __init__(self):
        # Internal pool of API keys (replace with actual keys in production)
        self.api_keys = ["khalid", "A1", "B2"]
        # Rate limits: function -> {N: requests, T: seconds}
        self.rate_limits = {
            'get_likes': {'N': 10, 'T': 21600},  # 10 requests per 6 hours
            'get_info': {'N': 100, 'T': 60},     # 100 requests per minute
            'check_ban': {'N': 1000, 'T': 60},   # 1000 requests per minute
        }
        # Rate limit queues: function -> api_key -> deque of timestamps
        self.rate_limit_queues = {
            func: {api_key: deque(maxlen=limit['N']) for api_key in self.api_keys}
            for func, limit in self.rate_limits.items()
        }

    def get_available_api_key(self, function_name):
        """Select an API key that can make a request now or soonest."""
        rate_limit = self.rate_limits[function_name]
        N = rate_limit['N']
        T = rate_limit['T']
        now = time.time()
        available_keys = []

        for api_key in self.api_keys:
            queue = self.rate_limit_queues[function_name][api_key]
            # Clean up expired timestamps
            while queue and now - queue[0] > T:
                queue.popleft()
            if len(queue) < N:
                available_keys.append((api_key, 0))
            else:
                oldest = queue[0]
                wait_time = max(0, T - (now - oldest))
                available_keys.append((api_key, wait_time))

        # Find the key with the shortest wait time
        min_wait_time = min(wait for _, wait in available_keys)
        candidates = [(key, wait) for key, wait in available_keys if wait == min_wait_time]
        selected_api_key, _ = random.choice(candidates)
        return selected_api_key, min_wait_time

    def get_likes(self, region, uid):
        """Get likes for a user in a region."""
        function_name = 'get_likes'
        api_key, wait_time = self.get_available_api_key(function_name)
        if wait_time > 0:
            time.sleep(wait_time)
        url = f"https://likes.api.v2.cloudenginexe.com/cloudlike?region={region}&uid={uid}&api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        self.rate_limit_queues[function_name][api_key].append(time.time())
        return response.json()

    def get_info(self, region, uid):
        """Get user information for a region."""
        function_name = 'get_info'
        api_key, wait_time = self.get_available_api_key(function_name)
        if wait_time > 0:
            time.sleep(wait_time)
        url = f"https://info.api.cloudenginexe.com/api/info?api_key={api_key}&region={region}&uid={uid}"
        response = requests.get(url)
        response.raise_for_status()
        self.rate_limit_queues[function_name][api_key].append(time.time())
        return response.json()

    def check_ban(self, uid):
        """Check if a user is banned."""
        function_name = 'check_ban'
        api_key, wait_time = self.get_available_api_key(function_name)
        if wait_time > 0:
            time.sleep(wait_time)
        url = f"https://bancheck.cloudenginecore.com/api/bancheck/{uid}?api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        self.rate_limit_queues[function_name][api_key].append(time.time())
        return response.json()