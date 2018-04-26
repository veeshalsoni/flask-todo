from flask import render_template, url_for, redirect, request, flash, jsonify
from app import app,db, csrf
from form import LoginForm, SignUpForm, TaskForm, DatePostsForm	
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Tasks
from werkzeug.urls import url_parse
from datetime import datetime
from flask_wtf.csrf import CSRFError


@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/signin", methods=['GET','POST'])
def signin():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash("Invalid username/password combination")
			return redirect(url_for('signin'))
		login_user(user,remember = form.remember.data)

		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			return redirect(url_for('home'))
		return redirect(url_for(next_page))
	return render_template("signin.html", form=form)

@app.route("/signup", methods=['GET','POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = SignUpForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()

		if user is not None:
			flash("User with email id already exist")
			return redirect('signup')

		user = User(username = form.username.data,email = form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("You have been successfully registered : " + form.username.data)
		return redirect(url_for('signin'))
	return render_template('signup.html', form = form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))

@login_required
@csrf.exempt
@app.route("/addtask",methods=['POST'])
def addtask():
	Taskform = TaskForm()
	if Taskform.is_submitted():
		dt = Taskform.taskdate.data
		if dt < datetime.date(datetime.today()):
			return jsonify({'Error' : 'Can not add task for past' })

		task = Tasks(user = current_user,text = Taskform.text.data, date = dt,category = Taskform.category.data)
		db.session.add(task)
		db.session.commit()
		return jsonify({'Success' : 'Task Added to your calender','id' : task.id })
	return jsonify({'Error' : 'Something Went Wrong, Try Again!','id' : task.id })

@login_required
@csrf.exempt
@app.route("/taskcompleted",methods = ['POST'])
def taskcompleted():
	try:
		id = request.form['id']
		id = id.split("-")[-1]
		task = Tasks.query.get(id)
		task.completed = not task.completed
		db.session.commit()
		if task.completed:
			status = "Task Marked As Completed"
		else:
			status = "Task Marked As Incomplete"
	except:
		status = "Sorry! Something went wrong, Try Again"
	return jsonify({'status' : status})

@login_required
@csrf.exempt
@app.route("/deletetask",methods = ['POST'])
def deletetask():
	try:
		id = request.form['id']
		id = id.split("-")[-1]
		task = Tasks.query.filter_by(id = id).delete()
		db.session.commit()
		status = "Task Successfully Deleted"
	except:
		status = "Sorry! Something went wrong, Try Again"
	return jsonify({'status' : status})

@login_required
@app.route("/home",methods=['GET','POST'])
def home():
	Taskform = TaskForm()
	DatePostsform = DatePostsForm()
	dt = DatePostsform.date.data
	dt = datetime(dt.year,dt.month,dt.day)
	dt = dt.replace(minute=0, hour=0, second=0, microsecond=0)
	tasks = Tasks.query.filter_by(user = current_user, date = dt)

	return render_template('home.html', tasks = tasks, Taskform = Taskform,DatePostsform = DatePostsform)

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'),404

@app.errorhandler(500)
def not_found_error(error):
	db.session.rollback()
	return render_template('500.html'),500