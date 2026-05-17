from resilient_client.retry import retry

call_count = 0

@retry(max_retries=3)
def flaky():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ValueError("not ready")
    return "success"

print(flaky())