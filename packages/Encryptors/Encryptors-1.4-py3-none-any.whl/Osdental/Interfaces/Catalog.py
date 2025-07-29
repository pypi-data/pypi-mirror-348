from pydantic import BaseModel
from typing import Optional

class Catalog(BaseModel):
    idCatalog: int
    nameCatalog: str
    idDetail: str
    code: str
    value: Optional[str] = None
