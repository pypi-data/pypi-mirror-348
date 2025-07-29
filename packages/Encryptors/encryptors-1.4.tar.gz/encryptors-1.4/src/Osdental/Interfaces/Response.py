from typing import Optional
from pydantic import BaseModel

class Response(BaseModel):
    status: str
    message: str
    data: Optional[str] = None 

    def to_json(self) -> str:
        return self.model_dump(mode='json')