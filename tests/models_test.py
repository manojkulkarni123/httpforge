from src.resilient_client.models import ClientConfig


c1 = ClientConfig(base_url="https://api.openai.com", method="POST")
c2 = ClientConfig(base_url="https://api.openai.com", method="POST")

print(c1 == c2)         
print(c1 is c2)        
print(c1.headers is c2.headers)  