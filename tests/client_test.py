import asyncio
from resilient_client.models import ClientConfig
from resilient_client.client import ResilientClient

async def main():
    config = ClientConfig(base_url="https://httpbin.org", method="GET")
    
    async with ResilientClient(config) as client:
        result = await client.request("/get")
        print(result)

asyncio.run(main())
