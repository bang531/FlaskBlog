import os

class Config:
	# secret key to prevent x-browser attack etc.
	SECRET_KEY = '828691f3ec80f5c69a48c401eb5404f9'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # location of Sqlite db

	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	# preferred way
	MAIL_USERNAME = os.environ.get('MSU_EMAIL_ADDR')
	MAIL_PASSWORD = os.environ.get('MSU_EMAIL_PWD')


