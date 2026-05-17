from dataclasses import replace
import httpx
from resilient_client.models import ClientConfig
from resilient_client.async_retry import async_retry

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

        @async_retry(max_retries=self.config.max_retries)
        async def _do():
            url = self.config.base_url + endpoint
            response = await self._session.request(
                method=self.config.method,
                url=url,
                headers=self.config.headers,
                timeout=self.config.timeout,
                json=body
            )
            response.raise_for_status()
            return response.json()
        
        return await _do()
