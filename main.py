import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/case_study'
db = SQLAlchemy(app)

class Registration(db.Model):
	c_id = db.Column(db.Integer, unique=True, primary_key=True)
	fname = db.Column(db.String, nullable=False)
	lname = db.Column(db.String, nullable=False)
	contact = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	pwd = db.Column(db.String, nullable=False)

	def __init__(self,c_id,fname,lname,contact,email,pwd):
		self.c_id = c_id
		self.fname = fname
		self.lname = lname
		self.contact = contact
		self.email = email
		self.pwd = pwd

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/login")
def login():
	if(request.method == "POST"):
		pass
	else:
		return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if(request.method == "POST"):
		c_id = 12345
		fname = request.form.get('fname')
		lname = request.form.get('lname')
		contact = request.form.get('contact')
		email = request.form.get('email')
		pwd = request.form.get('pwd')

		usr = Registration(c_id,fname,lname,contact,email,pwd)
		db.session.add(usr)
		db.session.commit()

		return render_template('login.html')

	else:
		return render_template('register.html')

app.run(debug=True)