"""Flask configuration variables."""
from os import environ, path
class Config:
    """Set Flask configuration from .env file."""

    # Database
    SQLALCHEMY_DATABASE_URI = 'mysql://webadmin:'+environ.get('MYSQL_DATABASE_PASSWORD')+'@helperdrive.tk/helper_drive'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False