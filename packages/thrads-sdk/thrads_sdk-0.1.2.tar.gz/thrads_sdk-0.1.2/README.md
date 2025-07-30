# Thrads SDK

Python SDK for integrating with the Thrads ad platform API.

## Installation

```bash
pip install thrads_sdk
```

## Basic Usage

```python
from thrads import ThradsClient

# Initialize client
client = ThradsClient(api_key="your_api_key")

# Get an ad recommendation
ad = client.get_ad(
    user_id="user123",
    chat_id="chat456",
    content={
        "user": "I need help finding a good math learning app",
        "chatbot": "What specific area of math are you interested in?"
    },
    user_region="US"
)

if ad:
    print(f"Recommended product: {ad.prod_name}")
    print(f"Creative message: {ad.creative}")
    print(f"URL: {ad.prod_url}")
    print(f"Image URL: {ad.img_url}")  # Base64 encoded image
else:
    print("No ad recommendation available")
```

## Advanced Usage

```python
from thrads import ThradsClient
import os
import time

# Initialize with environment variable
client = ThradsClient(api_key=os.environ.get("THRADS_API_KEY"))

# Generate unique IDs
timestamp = int(time.time())
user_id = f"user_{timestamp}"
chat_id = f"chat_{timestamp}"

# Get an ad with all optional parameters
ad = client.get_ad(
    user_id=user_id,
    chat_id=chat_id,
    content={
        "user": "I need help finding a good math learning app",
        "chatbot": "What specific area of math are you interested in?"
    },
    user_region="US",              # ISO 3166-1 alpha-2 country code
    meta_data={                    # Optional user metadata
        "device": "mobile",
        "browser": "chrome",
        "age_range": "18-24"
    },
    production=False,              # Set to True in production environments
    conversation_offset=2,         # Minimum turns before first ad
    ad_frequency_limit=5,          # Minimum turns between ads
    ad_aggressiveness="high",      # Ad matching flexibility: "low", "medium", "high"
    force=True                     # Force ad serving if possible
)

# Access response metadata
print(f"Request ID: {client.last_request_id}")
print(f"API Version: {client.api_version}")
print(f"Response Time: {client.last_response_time}ms")
print(f"Timestamp: {client.timestamp}")

# Display ad if available
if ad:
    print(f"Ad Creative: {ad.creative}")
    print(f"Product: {ad.prod_name}")
    print(f"URL: {ad.prod_url}")

    # Optionally convert base64 image to PIL Image
    image = ad.get_image()
    if image:
        # Display or save the image
        image.show()  # Opens in default image viewer
        # image.save("ad_image.png")
```

## Error Handling

```python
from thrads import ThradsClient, ThradsError, AuthenticationError, APIError

client = ThradsClient(api_key="your_api_key")

try:
    ad = client.get_ad(
        user_id="user123",
        chat_id="chat456",
        content={
            "user": "Help me find a good product",
            "chatbot": "What type of product are you looking for?"
        }
    )

    if ad:
        print(f"Ad served: {ad.prod_name}")
    else:
        print("No ad was served")

except AuthenticationError:
    print("Authentication failed - check your API key")
except RateLimitExceeded as e:
    print(f"Rate limit exceeded: {e}. Try again later.")
    print(f"Request ID for support: {e.request_id}")
except APIError as e:
    print(f"API error ({e.status_code}): {e}")
except NetworkError:
    print("Network connectivity issue - check your internet connection")
except ThradsError as e:
    print(f"General error: {e}")
```

## Features

- Simple, intuitive API for ad integration
- Automatic error handling and request retries
- Typed responses for improved code completion
- Detailed response metadata
- Support for image conversion from base64
- Comprehensive parameter options for fine-tuned ad serving

## Documentation

For more information about the Thrads API, visit [Thrads Documentation](https://thrads.ai/documentation).
