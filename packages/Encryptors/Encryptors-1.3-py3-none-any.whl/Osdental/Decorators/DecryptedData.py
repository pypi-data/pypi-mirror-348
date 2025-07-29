from functools import wraps
from typing import Callable, Type, Optional, Union
from pydantic import BaseModel, ValidationError
from Osdental.Encryptor.Jwt import JWT
from Osdental.Exception.ControlledException import UnauthorizedException, RequestDataException
from Osdental.Handlers.DBSecurityQuery import DBSecurityQuery
from Osdental.Handlers.Instances import jwt_user_key, aes
from Osdental.Interfaces.Token import AuthToken
from Osdental.Utils.Message import Message

db_security_query = DBSecurityQuery()

def process_encrypted_data(model: Optional[Type[BaseModel]] = None):
    def decorator(func:Callable):
        @wraps(func)
        async def wrapper(self, user_token_encrypted:str = None, aes_data:str = None, **rest_kwargs): 
            legacy = await db_security_query.get_data_legacy()
            token = None
            if user_token_encrypted:
                user_token = aes.decrypt(legacy.aesKeyUser, user_token_encrypted)
                token = AuthToken(**JWT.extract_payload(user_token, jwt_user_key))
                is_auth = await db_security_query.validate_auth_token(token.idToken, token.idUser)
                if not is_auth:
                    raise UnauthorizedException(message=Message.PORTAL_ACCESS_RESTRICTED_MSG, error=Message.PORTAL_ACCESS_RESTRICTED_MSG)
                
                token.jwtUserKey = jwt_user_key
                token.legacy = legacy

            data: Union[dict, BaseModel, None] = None
            if aes_data:
                decrypted_data = aes.decrypt(legacy.aesKeyAuth, aes_data)
                if model:
                    try:
                        data = model(**decrypted_data)
                    except ValidationError as e:
                        error_messages = [
                            f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
                            for err in e.errors()
                        ]
                        formatted_error = " | ".join(error_messages)
                        raise RequestDataException(message=Message.INVALID_REQUEST_PARAMS_MSG, error=f'Invalid data format: {formatted_error}')
                else:
                    data = decrypted_data
                

            return await func(self, data=data, token=token, **rest_kwargs)  
        
        return wrapper
    return decorator