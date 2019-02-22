import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
	#randomize file name using hex
	random_hex= secrets.token_hex(8) # random hex
	# ignore the filename part by using underscore (_)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn= random_hex + f_ext
	# save picture path to ../static/profile_pics
	picture_path= os.path.join(current_app.root_path,'static/profile_pics', picture_fn)
	# resize image using PIL
	output_size=(125,125) # pixel
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path) # save this thumbnail instad
	# form_picture.save(picture_path)  #old code
	return picture_fn
	pass

def send_reset_email(user):
	token= user.get_reset_token()
	msg= Message('Password Reset Request',
		sender='noreplydemo.com',
		recipients = [user.email])
# note _external=True gives the ABSOLUTE URL not relative URL
	msg.body = f'''To reset password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email

'''
	mail.send(msg)
	pass

