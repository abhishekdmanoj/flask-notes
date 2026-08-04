import os

class Config:
	SECRET_KEY = os.getenv("SECRET_KEY")

class TestingConfig(Config):
	TESTING = True

class ProductionConfig(Config):
	DEBUG = False
