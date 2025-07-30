# tests/test_integration.py
import os
import pytest
import time
from thrads import ThradsClient

# Skip all tests if API key is not provided
pytestmark = pytest.mark.skipif(
    not os.environ.get("THRADS_API_KEY"),
    reason="Integration tests require THRADS_API_KEY environment variable"
)


class TestThradsIntegration:
    def setup_method(self):
        # Get API key from environment
        api_key = os.environ.get("THRADS_API_KEY")

        # Optionally use different base URL for testing
        base_url = os.environ.get("THRADS_API_URL", "https://api.thrads.ai")

        self.client = ThradsClient(api_key=api_key, base_url=base_url)

    def test_real_api_call(self):
        """Test a real API call to the Thrads service."""
        # Generate unique user/chat IDs to avoid conflicts
        timestamp = int(time.time())
        user_id = f"test_user_{timestamp}"
        chat_id = f"test_chat_{timestamp}"

        # Make an actual API call
        ad = self.client.get_ad(
            user_id=user_id,
            chat_id=chat_id,
            content={
                "user": "I really want to learn math skills",
                "chatbot": "That's a great goal!"
            },
            user_region="US"
        )

        # We can't guarantee an ad will be served, so check response structure
        # rather than specific content
        if ad:
            print(ad)
            assert hasattr(ad, 'creative')
            assert hasattr(ad, 'prod_name')
            assert hasattr(ad, 'prod_url')

        # Verify metadata was captured regardless of whether an ad was served
        assert self.client.last_request_id is not None
        assert self.client.api_version is not None
