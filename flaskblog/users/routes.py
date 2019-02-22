from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users',__name__)

@users.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	rform = RegistrationForm()
	if rform.validate_on_submit():
		# has the password
		hashed_pwd= bcrypt.generate_password_hash(rform.password.data).decode('utf-8')
		user = User(
				username = rform.username.data
				,email = rform.email.data
				,password = hashed_pwd
			)
		db.session.add(user)
		db.session.commit()
		flash(f'Account has been created for {rform.username.data}. You can login','success')
		return redirect(url_for('users.login')) # redirect to login
	return render_template('register.html', title ='Register', form=rform)

@users.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	lform = LoginForm()
	if lform.validate_on_submit():
		user = User.query.filter_by(email=lform.email.data).first()
		# check if user & password matches
		if user and bcrypt.check_password_hash(user.password, lform.password.data):
			login_user(user, lform.remember.data)
			next_page=request.args.get('next') # use this not [] as 'next' arg is optional
			# go to page given by query parm next if it exists after login
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
		# if lform.email.data == 'admin1@blog.com' and lform.password.data == 'password':
		# 	flash(f'You are logged in as {lform.email.data}','success')
		# 	return redirect(url_for('home'))
		# else:
			flash('Login failed. Check email and/or password','danger')
	return render_template('login.html', title ='Login',form=lform)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))
	pass

# this reoute is only visible for login user
# login_required together with login_manager.login_view
@users.route('/account',methods=['GET','POST'])
@login_required
def account():
	aform = UpdateAccountForm()
	if aform.validate_on_submit():
		if aform.picture.data: # check if form submitted
			picture_file=save_picture(aform.picture.data)
			current_user.image_file=picture_file # update current user image file

		current_user.username=aform.username.data
		current_user.email=aform.email.data
		db.session.commit()
		flash('Your account has been updated','success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		aform.username.data = current_user.username
		aform.email.data = current_user.email

	image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title = 'Account'
		, image_file=image_file, form=aform)

# post for specific user
@users.route("/user/<string:username>")
def user_posts(username):
	# get page # via a get
	page=request.args.get('page',1,type=int) # default is 1
	user= User.query.filter_by(username=username).first_or_404()
	posts=Post.query.filter_by(author=user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=4) # previousle used all()
	return render_template('user_posts.html',posts=posts,user=user)
	pass

@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
	# has to logout to request password
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form=RequestResetForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		#send the password reset to the user with his email
		send_reset_email(user)
		flash('Email has been sent with instructions to reset password.','info')
		return redirect(url_for('users.login'))

	return render_template('reset_request.html',title='Reset Password', form=form)
	pass


@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
	# has to logout to request password
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))

	form = ResetPasswordForm()
	if form.validate_on_submit():
		# has the password
		hashed_pwd= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password= hashed_pwd
		
		db.session.commit()
		flash(f'Password has been reset. You can login','success')
		return redirect(url_for('users.login')) # redirect to login	
	return render_template('reset_token.html',title='Reset Password', form=form)
	pass

