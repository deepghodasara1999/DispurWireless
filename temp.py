import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import math
import random

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'dispurwireless@gmail.com',
    MAIL_PASSWORD='Dispur@2020',
	MAIL_DEFAULT_SENDER = 'dispurwireless@gmail.com'
)
mail = Mail(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/dispurwireless'
db = SQLAlchemy(app)

class Customer(db.Model):
	__tablename__='customer'
	customer_id = db.Column(db.Integer, unique=True, primary_key=True)
	first_name = db.Column(db.String, nullable=False)
	last_name = db.Column(db.String, nullable=False)
	mobile_no = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	address = db.Column(db.String, nullable=False)

	def __init__(self,first_name,last_name,mobile_no,email,password,address):
		self.first_name = first_name
		self.last_name = last_name
		self.mobile_no = mobile_no
		self.email = first_name
		self.password = password
		self.address = address

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

class Verify():
	customerObj=None
	CustomerOTP=None


@app.route("/")
def home():
	return render_template('index.html')

@app.route("/login")
def login():
	if(request.method == "POST"):
		id = request.form.get('email')
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
	if(request.method == "POST"):
		if request.form["btn"]=="register":
			fname = request.form.get('fname')
			lname = request.form.get('lname')
			contact = request.form.get('contact')
			email = request.form.get('email')
			pwd = request.form.get('pwd')
			address = request.form.get('address')
			customerObj = Customer(first_name=fname, last_name=lname, mobile_no=contact, email=email, password=pwd, address=address)
			Verify.customerObj = customerObj
 
			OTP = math.floor(random.random()*1000000)
			mail.send_message('Email Verification',
                          recipients = [email,],
                          body = "Your OTP is : " + str(OTP)
                          )
			Verify.CustomerOTP = OTP
			##--> code for invalid id

			return render_template('verify.html')
			
		else:
			if request.form.get('otp') == str(Verify.CustomerOTP):
				db.session.add(Verify.customerObj)
				db.session.commit()
				##--> code for send coustomer Id
				return render_template('confirm.html')
			else:
				##--> code here for wrong OTP
				return redirect("/register")

	else:
		return render_template('register.html')

@app.route("/admin", methods=['GET', 'POST'])
def admin():
	if (request.method == "POST"):
		return redirect("/admin-panel")
	else:
		return render_template("admin.html")

@app.route("/admin-panel", methods=['GET', 'POST'])
def admin():
	if (request.method == "POST"):
		pass
	else:
		return render_template("admin_panel.html")

app.run(debug=True)