class ResilientClientError(Exception):
    """Base exception for resilient-client"""

class NetworkError(ResilientClientError):
    """Connection or DNS failure"""

class TimeoutError(ResilientClientError):
    """Timeout error server not responding"""

class RateLimitError(ResilientClientError):
    """Request has been rate limited"""

class ServerError(ResilientClientError):
    """Server error"""

class ClientError(ResilientClientError):
    """Client side error"""

class PayloadError(ResilientClientError):
    """Payload wrong/incomplete"""

