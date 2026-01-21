import os

APP_NAME = os.environ.get('APP_NAME', 'productivity-api')
APP_VERSION = os.environ.get('APP_VERSION', '1.0')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./app.db')
