import random
import string
import re
from datetime import datetime, timedelta
from Osdental.Interfaces.Response import Response
from Osdental.Utils.Code import Code
from Osdental.Utils.Message import Message

class Util:
    
    @staticmethod
    def response(status:str = Code.PROCESS_SUCCESS_CODE, message:str = Message.PROCESS_SUCCESS_MSG, data:str = None):
        return Response(status=status, message=message, data=data).to_json()

    @staticmethod
    def generate_password(length: int = 12) -> str:
        valid_characters = string.ascii_letters + string.digits + '!@#$%^&*()-_=+[]{}|:,.?'
        password = ''.join(random.choice(valid_characters) for _ in range(length))
        return password
    
    @staticmethod
    def generate_numeric_code(length:int = 6) -> str:
        nums = string.digits        
        return ''.join(random.choices(nums,k=length)) 
    
    @staticmethod
    def generate_alpha_code(length:int = 6) -> str:
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    @staticmethod
    def generate_uppercase_code(length:int = 6) -> str:
        return ''.join(random.choices(string.ascii_uppercase, k=length))
    
    @staticmethod
    def generate_lowercase_code(length:int = 6) -> str:
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    @staticmethod
    def generate_alphanumeric_code(length: int = 6) -> str:
        chars = string.ascii_letters + string.digits  
        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def generate_secure_code(length: int = 6) -> str:
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(chars, k=length))

    @staticmethod
    def concat_str(*args):
        return ' '.join(str(arg) for arg in args).strip()
    
    @staticmethod
    def clean_str(text:str):
        text = text.lower()
        text = text.strip()
        text = re.sub(r'\s+', '_', text)
        text = re.sub(r'[^a-z0-9 ]', '', text)
        return text
    
    @staticmethod
    def get_ttl_for_midnight():
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        midnight = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day)
        ttl = (midnight - now).seconds
        return ttl
