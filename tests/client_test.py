from src.resilient_client.client import ResilientClient
from src.resilient_client.models import ClientConfig

config = ClientConfig(base_url="https://api.openai.com", method="POST")
client = ResilientClient(config)

print(client)
client()

client2 = client.update_headers({"Authorization": "Bearer sk-123"})
print(client2)
print(client is client2)
print(client.config.headers)
print(client2.config.headers)

