from dataclasses import replace
import httpx
from resilient_client.models import ClientConfig
from resilient_client.async_retry import async_retry
from resilient_client.logger import get_logger
from resilient_client.exceptions import (
    NetworkError,
    TimeoutError,
    RateLimitError,
    ServerError,
    ClientError,
)

logger = get_logger()

class ResilientClient:
    def __init__(self, config: ClientConfig):

        self.config= config
        self._request_count=0

    def __repr__(self):
        return f"ResilientClient(base_url='{self.config.base_url}',method='{self.config.method}',requests_made={self._request_count})"

    def __call__(self):
        print(f"Client ready at {self.config.base_url}")

    def update_headers(self,new_headers:dict[str,str])->"ResilientClient":

        merged = {**self.config.headers, **new_headers}
        new_config =  replace(self.config,headers=merged)
        return ResilientClient(new_config)

    async def __aenter__(self):
     self._session = httpx.AsyncClient()
     return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.aclose()
        return False
    
    async def request(self, endpoint: str, body: dict = None) -> dict:
        self._request_count += 1
        logger.info("request_started", endpoint=endpoint, method=self.config.method)

        @async_retry(max_retries=self.config.max_retries,exceptions=(NetworkError, TimeoutError, ServerError))
        async def _do():
            url = self.config.base_url + endpoint
            try:
                response = await self._session.request(
                    method=self.config.method,
                    url=url,
                    headers=self.config.headers,
                    timeout=self.config.timeout,
                    json=body
                )
                response.raise_for_status()
                logger.info("request_success", endpoint=endpoint, status=response.status_code)
                return response.json()
            except httpx.TimeoutException:
                raise TimeoutError(f"Request to {url} timed out")
            except httpx.ConnectError:
                raise NetworkError(f"Could not connect to {url}")
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    raise RateLimitError("Rate limit hit")
                elif e.response.status_code >= 500:
                    raise ServerError(f"Server error: {e.response.status_code}")
                else:
                    raise ClientError(f"Client error: {e.response.status_code}")
            
        return await _do()

    async def paginate(self,endpoint:str):
        page=1
        while True:
            data = await self.request(f"{endpoint}?page={page}")
            yield data["items"]
            if not data.get("next_page"):
                break
            page += 1