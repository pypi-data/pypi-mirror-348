from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from Osdental.Interfaces.Legacy import Legacy

class AuthToken(BaseModel):
    idToken: Optional[UUID] = None
    idUser: Optional[UUID] = None
    idExternalEnterprise: Optional[UUID] = None
    idProfile: Optional[UUID] = None
    idLegacy: Optional[UUID] = None
    idItemReport: Optional[UUID] = None
    idEnterprise: Optional[UUID] = None
    idAuthorization: Optional[UUID] = None
    userFullName: Optional[str] = None
    abbreviation: Optional[str] = None
    aesKeyAuth: Optional[str] = None
    jwtUserKey: Optional[str] = None
    legacy: Optional[Legacy] = None