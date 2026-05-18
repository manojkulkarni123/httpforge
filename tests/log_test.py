import asyncio
from resilient_client import ResilientClient, ClientConfig
from resilient_client.exceptions import ResilientClientError

async def main():
    config = ClientConfig(base_url="https://httpbin.org", method="GET")
    
    async with ResilientClient(config) as client:
        # successful request
        result = await client.request("/get")
        print("---")
        # trigger an error
        try:
            await client.request("/status/429")
        except ResilientClientError as e:
            print(f"Caught: {type(e).__name__}: {e}")

asyncio.run(main())