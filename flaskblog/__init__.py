# import os # not used
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # hash
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# mail server, port tls etc.

db= SQLAlchemy() # set up the db without any app first
bcrypt=Bcrypt() # bcrypt class
login_manager = LoginManager()
login_manager.login_view = 'users.login' # set login route 'login' - is function
login_manager.login_message_category='info' # set msg category


mail = Mail()

def create_app(config_class=Config):
	app=Flask(__name__)
	app.config.from_object(Config) # config comes from class Config

	db.init_app(app) # init the extension with the app object
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	# has to be here to prevent circular referencing
	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main

	from flaskblog.errors.handlers import errors

	# register blueprint
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)
	
	return app