import os
from datetime import timedelta
from dotenv import load_dotenv

# load environment variables from.env file
load_dotenv()


class Config:
    """Base configuration class"""

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security Configuration
    SECRET_KEY = os.environ.get('SERCRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')

    # JWT Token Expiration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # CORS Configuration
    CORS_HEADERS = 'Content-Type'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProdustionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'


# Configuration disctionary
config = {
    'development': DevelopmentConfig,
    'production': ProdustionConfig,
    'default': DevelopmentConfig
}
