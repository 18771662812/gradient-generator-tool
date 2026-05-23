import os
from dataclasses import dataclass


@dataclass
class Config:
    DB_HOST: str = os.environ.get('DATABASE_HOST', 'localhost')
    DB_PORT: int = int(os.environ.get('DATABASE_PORT', 5432))
    DB_NAME: str = os.environ.get('DATABASE_NAME', 'postgres')
    DB_USER: str = os.environ.get('DATABASE_USER', 'gaussdb')
    DB_PASSWORD: str = os.environ.get('DATABASE_PASSWORD', 'OpenGauss@2024')
    
    JWT_SECRET: str = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRATION_DAYS: int = 7


config = Config()
