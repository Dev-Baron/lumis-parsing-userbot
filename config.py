import os
from pathlib import Path
from dotenv import load_dotenv

class SecConfig:

    def __init__(self):
        
        if not Path('.env').exists():
            raise FileNotFoundError('Файл .env не был найден...')

        load_dotenv('.env')
        self.API_ID = os.getenv('API_ID')
        self.API_HASH = os.getenv('API_HASH')

        self._validate()
        
    def _validate(self):
        if not self.API_ID:
            raise ValueError('API_ID не был найден, пожалуйста, проверьте конфиг...')
        
        if not self.API_HASH:
            raise ValueError('API_HASH не был найден, пожалуйста, проверьте конфиг...')
        
Config = SecConfig()