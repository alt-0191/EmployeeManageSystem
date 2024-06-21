import secrets

username = 'root'
password = '123456'
connect = 'localhost'
database = 'xxcompany'


flask_secret_key = secrets.token_hex(16)


class Config:
    SECRET_KEY = flask_secret_key
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{connect}/{database}?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

