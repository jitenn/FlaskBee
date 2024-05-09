# Configuration file to store key variables
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# print(f"basedir %", basedir)

load_dotenv(os.path.join(basedir, '.env'))
# print(os.path.join(basedir, '.env'))

class Config:
    
    # SECRET_KEY is used by flask to generate tokens and signatures to prevent
    # cross site request forgeries / CSRF / seasurf
    SECRET_KEY = os.environ.get("SECRET_KEY") or "JitensSuperSecretKey"
    
    # SQLALCHEMY_DATABASE_URI is needed by SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Heroku has an environment variable set for DATABASE_URL
    # postgres://u4kmr7cuddug18:p0c63e8cb520d7364666b6d83dc3dc829bacbd00f4b85f4c7a4fcd960a80a06f6@cb4l59cdg4fg1k.
    # cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d9dp4pfs6nsa4p
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Heroku related change to log to stdout 
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # Location of word dictionaries
    DICTIONARY_STATIC = "txtDictionary12Dicts.txt"
    DICTIONARY_DYNAMIC = "https://ia803406.us.archive.org/31/items/csw21/CSW21.txt"

    # Puzzle generation parameters
    LETTERS_TO_AVOID = "QS"
    BEES_MINIMUM = 20
    BEES_MAXIMUM = 50

