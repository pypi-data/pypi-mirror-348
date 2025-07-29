from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Legacy(BaseModel):
    idLegacy: Optional[UUID] = None
    legacyName: Optional[str] = None
    idEnterprise: Optional[UUID] = None
    refreshTokenExpMin: Optional[int] = None
    accessTokenExpMin: Optional[int] = None
    publicKey2: Optional[str] = None
    privateKey1: Optional[str] = None
    privateKey2: Optional[str] = None
    aesKeyUser: Optional[str] = None
    aesKeyAuth: Optional[str] = None