# test_api.py
from thrads import ThradsClient, AsyncThradsClient
import os
import time
import asyncio
import sys

# Get API key from environment
api_key = os.environ.get("THRADS_API_KEY")
if not api_key:
    print("Please set THRADS_API_KEY environment variable")
    exit(1)

# Check if --no-verify flag is passed
verify_ssl = "--no-verify" not in sys.argv

# Test timestamp to make unique IDs
timestamp = int(time.time())

# Synchronous API test


def test_sync_api():
    print("\n--- Testing Synchronous API ---")
    client = ThradsClient(api_key=api_key)

    # Make an actual API call
    ad = client.get_ad(
        user_id=f"test_user_{timestamp}_sync",
        chat_id=f"test_chat_{timestamp}_sync",
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
        print(f"Request ID: {client.last_request_id}")
        print(f"Response Time: {client.last_response_time}")
    else:
        print("No ad was served")

    return ad

# Asynchronous API test


async def test_async_api():
    print("\n--- Testing Asynchronous API ---")
    print(f"SSL Verification: {'Enabled' if verify_ssl else 'Disabled'}")
    async with AsyncThradsClient(api_key=api_key, verify_ssl=verify_ssl) as client:
        # Make an async API call
        ad = await client.get_ad(
            user_id=f"test_user_{timestamp}_async",
            chat_id=f"test_chat_{timestamp}_async",
            content={
                "user": "I really want to learn maths skills",
                "chatbot": "Amazing! What area of math are you looking to improve in?"
            },
            user_region="US",
            force=True  # Force an ad if possible
        )

        # Print response
        if ad:
            print(f"Ad Creative: {ad.creative}")
            print(f"Product: {ad.prod_name}")
            print(f"URL: {ad.prod_url}")
            print(f"Request ID: {client.last_request_id}")
            print(f"Response Time: {client.last_response_time}")
        else:
            print("No ad was served")

        return ad

# Comparison test with multiple async requests


async def test_multiple_async_requests():
    print("\n--- Testing Multiple Async Requests ---")
    start_time = time.time()

    async with AsyncThradsClient(api_key=api_key, verify_ssl=verify_ssl) as client:
        tasks = []
        # Create 3 simultaneous requests
        for i in range(3):
            task = client.get_ad(
                user_id=f"test_user_{timestamp}_multi_{i}",
                chat_id=f"test_chat_{timestamp}_multi_{i}",
                content={
                    "user": f"I want to learn {'math' if i == 0 else 'coding' if i == 1 else 'drawing'}",
                    "chatbot": "That's great! What's your current skill level?"
                },
                user_region="US",
                force=True
            )
            tasks.append(task)

        # Execute all requests concurrently
        results = await asyncio.gather(*tasks)

        # Print results
        print(
            f"Completed {len(results)} requests in {time.time() - start_time:.2f} seconds")
        for i, ad in enumerate(results):
            if ad:
                print(f"\nRequest {i+1}:")
                print(f"Ad Creative: {ad.creative}")
                print(f"Product: {ad.prod_name}")
            else:
                print(f"\nRequest {i+1}: No ad was served")

# Main function to run all tests


async def main():
    # Run sync test first
    sync_ad = test_sync_api()

    # Then run async tests
    async_ad = await test_async_api()

    # Finally run multiple async requests
    await test_multiple_async_requests()

    print("\n--- Test Summary ---")
    print(f"Sync API test: {'Successful' if sync_ad else 'No ad served'}")
    print(f"Async API test: {'Successful' if async_ad else 'No ad served'}")

# Run all tests
if __name__ == "__main__":
    if "--no-verify" in sys.argv:
        print("Warning: SSL verification disabled - use only for testing!")
    asyncio.run(main())
