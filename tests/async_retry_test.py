from resilient_client.async_retry import async_retry


import asyncio

call_count = 0

@async_retry(max_retries=3)
async def flaky():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ValueError("not ready")
    return "success"

async def main():
    result = await flaky()
    print(result)

asyncio.run(main())