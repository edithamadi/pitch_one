import os

class Config:
   SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://edith:JASMINE5e@localhost/minutepitch'

   pass
class ProdConfig(Config):
   pass
class DevConfig(Config):
   SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://edith:edith:JASMINE5e@localhost/minutepitch'
   DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}