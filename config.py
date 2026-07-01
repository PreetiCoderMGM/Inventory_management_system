import os

LOW_STOCK_THRESHOLD = 5


class Config:
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'mysql+mysqlconnector://root:root@localhost/inventory_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-dev-key'
