#A decorator is essentially a function that takes another function as an argument and returns a new function with enhanced functionality.

import time
from functools import wraps

def retry(max_retries: int = 3, exceptions: tuple = (Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    wait = 2 ** i
                    print(f"Attempt number {i+1} failed {e}, wait for {wait} Seconds")
                    time.sleep(wait)
            raise last_exception 
        return wrapper
    return decorator
