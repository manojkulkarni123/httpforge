from dataclasses import replace

from resilient_client.models import ClientConfig

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

