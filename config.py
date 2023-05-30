import os
class Config(object):
    DIALECT = os.getenv('DB_DIALECT')
    USERNAME = os.getenv('DB_USERNAME')
    PASSWORD = os.getenv('DB_PASSWORD')
    HOST = os.getenv('DB_HOST')
    DATABASE = os.getenv('DB_DATABASE')
    #dialect://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = DIALECT+'://'+USERNAME+':'+PASSWORD+'@'+HOST+'/'+DATABASE