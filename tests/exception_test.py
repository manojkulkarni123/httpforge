import asyncio
from resilient_client.models import ClientConfig
from resilient_client.client import ResilientClient
from resilient_client.exceptions import ResilientClientError

async def main():
    config = ClientConfig(base_url="https://httpbin.org", method="GET")
    
    async with ResilientClient(config) as client:
        try:
            # httpbin returns 404 for this endpoint
            result = await client.request("/status/429")
            print(result)
        except ResilientClientError as e:
            print(f"Caught: {type(e).__name__}: {e}")

asyncio.run(main())