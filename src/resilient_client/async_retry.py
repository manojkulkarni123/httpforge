import asyncio
from functools import wraps

def async_retry(max_retries: int = 3, exceptions: tuple = (Exception,)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    wait = 2 ** i
                    print(f"Attempt number {i+1} failed {e}, wait for {wait} Seconds")
                    await asyncio.sleep(wait)
            raise last_exception 
        return wrapper
    return decorator
