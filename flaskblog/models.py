from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
	pass

# db Objects defined as classes
class User(db.Model, UserMixin):
	id= db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(20), unique=True, nullable=False)
	email=db.Column(db.String(120), unique=True, nullable=False)
	image_file=db.Column(db.String(20),nullable=True, default='default.jpg') # has default image
	password=db.Column(db.String(60), nullable=False)
# in relationship, target ie Post is referencing the Class, hence capitalize Post
	post= db.relationship('Post', backref = 'author', lazy=True)

	def get_reset_token(self,expires_sec=1800):
		s= Serializer(current_app.config['SECRET_KEY'],expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')
		pass

	@staticmethod
	def verify_reset_token(token):
		s= Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id=s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self): # how obj is preinted
		return f"User('{self.username}','{self.email}','{self.image_file}')"
	pass

class Post(db.Model):
	id= db.Column(db.Integer, primary_key=True)
	title=db.Column(db.String(100),nullable=False)
	date_posted=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
	content=db.Column(db.Text(100),nullable=False)
# specify foreign key to refer to user as the author
# note: ForiegnKey ref tablename and column name hence lower case user.id
	user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	def __repr__(self): # how obj is preinted
		return f"Post('{self.title}','{self.date_posted}')"
	pass

