from dotenv import load_dotenv
load_dotenv()
import os

APP_NAME = os.environ.get('APP_NAME', 'productivity-api')
APP_VERSION = os.environ.get('APP_VERSION', '1.0')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
DATABASE_URL = os.environ.get('DATABASE_URL')
JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = 'HS256'
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

if ENVIRONMENT == 'production' and not JWT_SECRET:
    raise RuntimeError('JWT_SECRET must be set in production environment')
