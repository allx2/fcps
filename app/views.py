from flask import render_template, flash, redirect, session, url_for, request
from flask.ext.login import login_user, logout_user, current_user, login_required 
from app import app, db, lm
from werkzeug import secure_filename
from .forms import LoginForm, UploadForm
from .models import User

import os

@app.route('/')
@app.route('/home')
def index():
    return render_template("base.html")

@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()

	if current_user.is_authenticated():
		flash("you're already logged in, " + current_user.username + "!")
		return redirect('/')
	
	if form.validate_on_submit():
		print('Login requested for user: %s pass: %s ' % (form.username.data, form.password.data) )
		user = User.query.filter_by(username = form.username.data).first()

		if user is not None:
			login_user(user)
			flash("Login successful!")
		else:
			print("Can't login: user", form.username.data, "doesn't exist.")

		return redirect('/')

	return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("logout successful")
	return redirect('/')

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/upload',methods=['GET','POST'])
@login_required
def upload():
	form = UploadForm()
 
	if form.validate_on_submit():
		filename = secure_filename(form.upload.data.filename)
		full_path = os.path.join(app.config['UPLOAD_PATH'],current_user.username)

		#make the user's upload directory if it doesn't exist
		if not os.path.exists(full_path):
			os.makedirs(full_path)

		full_path = os.path.join(full_path, filename)
		form.upload.data.save(full_path)
		flash("uploaded to " + full_path)
		
		return redirect("/")

	return render_template("upload.html",form=form)

