# Adgent SDK

Python SDK for integrating with the Thrads ad platform.

## Installation

```bash
pip install thrads-sdk
```

## Usage

```python
from thrads import ThradsClient

# Initialize client
client = ThradsClient(api_key="your_api_key")

# Get an ad recommendation
ad = client.get_ad(
    user_id="user123",
    chat_id="chat456",
    content="I need a new pair of running shoes",
    user_region="US"
)

if ad:
    print(f"Recommended product: {ad.prod_name}")
    print(f"Creative message: {ad.creative}")
    print(f"URL: {ad.prod_url}")
else:
    print("No ad recommendation available")
```

## Features

- Simple, intuitive API
- Automatic error handling
- Typed responses with Pydantic models
