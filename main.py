import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import math
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/case_study'
db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME='dispurwireless@gmail.com',
    MAIL_PASSWORD='Dispur@2020',
    MAIL_DEFAULT_SENDER='dispurwireless@gmail.com'
)
mail = Mail(app)

class Registration(db.Model):
	c_id = db.Column(db.Integer, unique=True, primary_key=True)
	fname = db.Column(db.String, nullable=False)
	lname = db.Column(db.String, nullable=False)
	contact = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	pwd = db.Column(db.String, nullable=False)
	street = db.Column(db.String, nullable=True)
	city = db.Column(db.String, nullable=True)
	state = db.Column(db.String, nullable=True)
	pincode = db.Column(db.String, nullable=True)

	def __init__(self,fname,lname,contact,email,pwd):
		self.fname = fname
		self.lname = lname
		self.contact = contact
		self.email = email
		self.pwd = pwd

class Plan(db.Model):
	name = db.Column(db.String, unique=True, primary_key=True)
	price = db.Column(db.Integer, nullable=False)
	account = db.Column(db.Integer, nullable=False)
	speed = db.Column(db.Integer, nullable=False)
	validity = db.Column(db.Integer, nullable=False)
	data = db.Column(db.String, nullable=True)

	def __init__(self,name,price,account,speed,validity,data):
		self.name = name
		self.price = price
		self.speed = speed
		self.account = account
		self.validity = validity
		self.data = data

class Admin(db.Model):
	__tablename__='admin'
	id = db.Column(db.String, primary_key=True)
	fname = db.Column(db.String, nullable=False)
	lname = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)

	def __init__(self,id,fname,lname,email,password):
		self.id = id
		self.fname = fname
		self.lname = lname
		self.email = email
		self.password = password

class CurrentAdmin:
	adminObj = None
	total= None
	userObjs = None
	givenId = None

class CurrentUser:
	usrObj =None

class Verify():
    customerObj = None
    CustomerOTP = None

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/login",  methods=['GET', 'POST'])
def login():
	if(request.method == "POST"):
		username = request.form.get('email')
		password = request.form.get('pwd')

		u = Registration.query.filter_by(c_id=username).first()
		if(str(u.c_id) == str(username) and u.pwd == password):
			CurrentUser.usrObj = u
			return redirect("/profile")
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if (request.method == "POST"):
		if request.form["btn"] == "register":
			fname = request.form.get('fname')
			lname = request.form.get('lname')
			contact = request.form.get('contact')
			email = request.form.get('email')
			pwd = request.form.get('pwd')
			customerObj = Registration(fname,lname,contact,email,pwd)
			Verify.customerObj = customerObj

			OTP = math.floor(random.random() * 1000000)
			mail.send_message('Email Verification',
							  recipients=[email, ],
							  body="Your OTP is : " + str(OTP)
							  )
			Verify.CustomerOTP = OTP
			##--> code for invalid id

			return render_template('verify.html')

		else:
			if request.form.get('otp') == str(Verify.CustomerOTP):
				print("I am here")
				db.session.add(Verify.customerObj)
				db.session.commit()
				##--> code for send coustomer Id
				mail.send_message('Registration Successful',
								  recipients=[Verify.customerObj.email, ],
								  body="Your Customer ID is : " + str(Verify.customerObj.c_id))
				return render_template('confirm.html')
			else:
				##--> code here for wrong OTP
				return redirect("/register")

	else:
		return render_template('register.html')

@app.route("/profile", methods=['GET', 'POST'])
def profile():
	if(request.method == "POST"):
		admin = Registration.query.filter_by(c_id=request.form['c_id']).first()
		if(request.form["flag"]=="contact"):
			CurrentUser.usrObj.contact = request.form.get('phn')
			admin.contact = request.form.get('phn')
			db.session.commit()
		elif (request.form["flag"]=="street"):
			CurrentUser.usrObj.street = request.form.get('street')
			admin.street = request.form.get('street')
			db.session.commit()
		elif (request.form["flag"]=="city"):
			CurrentUser.usrObj.city = request.form.get('city')
			admin.city = request.form.get('city')
			db.session.commit()
		elif (request.form["flag"]=="state"):
			CurrentUser.usrObj.state = request.form.get('state')
			admin.state = request.form.get('state')
			db.session.commit()
		elif (request.form["flag"]=="pincode"):
			CurrentUser.usrObj.pincode = request.form.get('pincode')
			admin.pincode = request.form.get('pincode')
			db.session.commit()
	return render_template('profile.html',user=CurrentUser.usrObj)

@app.route("/plans")
def plans():
	users = Plan.query.all()
	return render_template('plans.html',users=users)

@app.route("/status")
def status():
	return render_template('status.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
	if (request.method == "POST"):
		print("1")
		id = request.form.get('id')
		password = request.form.get('pwd')

		u = Admin.query.filter_by(id=id).first()
		if(str(u.id) == str(id) and u.password == password):
			print("2")
			CurrentAdmin.adminObj = u
			rows = Registration.query.filter().count()
			CurrentAdmin.total = rows
			return redirect("/admin_panel")
		else:
			print("3")
			return render_template('admin_login.html')
	else:
		print("4")
		return render_template("admin_login.html")

@app.route("/admin_panel", methods=['GET', 'POST'])
def admin_panel():
	if (request.method == "POST"):  #request from form
		if request.form["form_flag"]=="search": #search
			print("i am in search")
			given_id = int(request.form.get('given_id'))
			CurrentAdmin.givenId = given_id
			user = Registration.query.filter_by(c_id=given_id).first()
			if user is None:
				user = 0
			else:
				CurrentAdmin.userObjs = user
			return render_template("admin_panel.html", no = CurrentAdmin.total, flag = 1, id=given_id, user = user)
		elif request.form["form_flag"]=="delete": #delete
			print("I am in delete")
			db.session.delete(CurrentAdmin.userObjs)
			db.session.commit()
			rows = Registration.query.filter().count()
			CurrentAdmin.total = rows
			return render_template("admin_panel.html", no = CurrentAdmin.total, flag = 2, id=CurrentAdmin.givenId)
		else:
			print("i am in else")
	else: # first render
		return render_template("admin_panel.html", no = CurrentAdmin.total, flag = 0)

app.run(debug=True)