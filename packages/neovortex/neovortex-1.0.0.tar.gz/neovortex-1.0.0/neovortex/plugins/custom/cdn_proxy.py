from neovortex.request import NeoVortexRequest
from neovortex.exceptions import NeoVortexError
import random

class CDNProxyPlugin:
    """Routes requests through a CDN or proxy for faster responses."""
    
    def __init__(self, proxies: list[str]):
        if not proxies:
            raise NeoVortexError("At least one proxy required")
        self.proxies = proxies

    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        proxy = random.choice(self.proxies)
        request.headers["X-Proxy"] = proxy
        return request