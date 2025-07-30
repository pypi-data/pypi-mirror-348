# test_api.py
from thrads import ThradsClient
import os
import time

# Get API key from environment
api_key = os.environ.get("THRADS_API_KEY")
if not api_key:
    print("Please set THRADS_API_KEY environment variable")
    exit(1)

client = ThradsClient(api_key=api_key)
timestamp = int(time.time())

# Make an actual API call
ad = client.get_ad(
    user_id=f"test_user_{timestamp}",
    chat_id=f"test_chat_{timestamp}",
    content={
        "user": "I need help finding a good math learning app",
        "chatbot": "What specific area of math are you interested in?"
    },
    user_region="US",
    force=True  # Force an ad if possible
)

# Print response
if ad:
    print(f"Ad Creative: {ad.creative}")
    print(f"Product: {ad.prod_name}")
    print(f"URL: {ad.prod_url}")
else:
    print("No ad was served")
