from dataclasses import  field, dataclass
from typing import Literal



@dataclass(frozen=True)
class ClientConfig:
    base_url: str
    method: Literal["GET","POST","PUT","DELETE","PATCH"]
    headers: dict[str,str] = field(default_factory=dict)
    timeout: float = 30.0
    max_retries: int = 3


c1 = ClientConfig(base_url="https://api.openai.com", method="POST")
c2 = ClientConfig(base_url="https://api.openai.com", method="POST")

print(c1 == c2)         
print(c1 is c2)        
print(c1.headers is c2.headers)  