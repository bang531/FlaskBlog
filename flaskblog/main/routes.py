from flask import render_template, request, Blueprint
from flaskblog.models import Post

main= Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
	# get page # via a get
	page=request.args.get('page',1,type=int) # default is 1
	posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4) # previousle used all()
	return render_template('home.html',posts=posts)
	pass

@main.route('/about')
def about():
	""" About Page route function """
	return render_template('about.html', title='About')
	passmain