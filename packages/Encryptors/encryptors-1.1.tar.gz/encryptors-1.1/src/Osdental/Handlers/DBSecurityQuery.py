from uuid import UUID
from Osdental.Handlers.Instances import db_security
from Osdental.Interfaces.Legacy import Legacy
from Osdental.Exception.ControlledException import UnauthorizedException
from Osdental.Utils.Message import Message
from Osdental.Utils.Code import Code

class DBSecurityQuery:

    @staticmethod
    async def get_data_legacy() -> Legacy:
        data = await db_security.execute_query_return_data('EXEC SECURITY.sps_SelectDataLegacy', fetchone=True)
        return Legacy(**data)
    
    @staticmethod
    async def validate_auth_token(token_id:UUID, user_id:UUID) -> bool:
        query = """ 
        EXEC SECURITY.sps_ValidateUserToken  
        @i_idToken = :token_id,
        @i_idUser = :user_id
        """
        is_auth = await db_security.execute_query_return_first_value(query, {'token_id': token_id, 'user_id': user_id})
        if not is_auth:
            raise UnauthorizedException(message=Message.PORTAL_ACCESS_RESTRICTED_MSG, error=Message.PORTAL_ACCESS_RESTRICTED_MSG, status_code=Code.UNAUTHORIZATED_CODE)
            
        return is_auth