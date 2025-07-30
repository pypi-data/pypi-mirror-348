from neovortex.request import NeoVortexRequest
from neovortex.exceptions import NeoVortexError
import random

class APIKeyRotationPlugin:
    """Rotates API keys from a pool to avoid rate limits."""
    
    def __init__(self, api_keys: list[str], header_name: str = "X-API-Key"):
        if not api_keys:
            raise NeoVortexError("At least one API key required")
        self.api_keys = api_keys
        self.header_name = header_name
        self.current_key = random.choice(api_keys)

    def process_request(self, request: NeoVortexRequest) -> NeoVortexRequest:
        self.current_key = random.choice(self.api_keys)  # Rotate key
        request.headers[self.header_name] = self.current_key
        return request