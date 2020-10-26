import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template,request, redirect
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
	street = db.Column(db.String, nullable=False)
	city = db.Column(db.String, nullable=False)
	state = db.Column(db.String, nullable=False)
	pincode = db.Column(db.String, nullable=False)

	def __init__(self,fname,lname,contact,email,pwd):
		self.fname = fname
		self.lname = lname
		self.contact = contact
		self.email = email
		self.pwd = pwd

class CurrentUser:
	usrObj =None

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
	if(request.method == "POST"):
		fname = request.form.get('fname')
		lname = request.form.get('lname')
		contact = request.form.get('contact')
		email = request.form.get('email')
		pwd = request.form.get('pwd')

		usr = Registration(fname,lname,contact,email,pwd)
		db.session.add(usr)
		db.session.commit()

		return render_template('login.html')
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

app.run(debug=True)