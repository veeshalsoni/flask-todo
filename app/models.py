from app import db,login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64))
	email = db.Column(db.String(64), index = True, unique = True)
	password = db.Column(db.String(128))
	tasks = db.relationship('Tasks',backref = 'user', lazy = 'dynamic')

	def set_password(self,password):
		self.password = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password,password)  

	def __repr__(self):
		return '<user {} >'.format(self.username)

class Tasks(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	text = db.Column(db.String(128),nullable = False)
	category = db.Column(db.String(32))
	date = db.Column(db.DateTime, default = datetime.utcnow)
	completed = db.Column(db.Boolean, default = False)
	user_id = db.Column(db.Integer,db.ForeignKey(User.id))

	def __repr__(self):
		return '<post {} {} {}>'.format(self.text,self.date,self.category)
