from flask import Flask,render_template,request,session,redirect,url_for
from database import *
import demjson
import urllib
import numpy
import sklearn
from core import *
import uuid

app=Flask(__name__)
app.secret_key="val"

@app.route('/',methods=['get','post'])
def home():
	# val()

	return render_template('index.html')

@app.route('/register',methods=['get','post'])
def register():
	return render_template('register.html')

@app.route('/login',methods=['get','post'])
def login():
	return render_template('login.html')

@app.route('/user_home',methods=['get','post'])
def user_home():
	gets=val(session['user_id'])
	print(gets)
	if gets=="failed":
		return redirect(url_for('home'))
	return render_template('user_home.html')

@app.route('/validatingidcard',methods=['get','post'])
def validatingidcard():
	if 'submit' in request.form:
		image=request.files['image']
		path="static/checking/testocrfiles/fileocr.jpg"
		image.save(path)
		content=ocrgenerate(path)
		print("gh",content)
		lcontent=session['ocrfile']
		print("ghsg",lcontent)
		if lcontent==content:
			return redirect(url_for('user_home'))
		else:
			return redirect(url_for('home'))



	return render_template('validatingidcard.html')

@app.route('/userfaceegister',methods=['get','post'])
def userfaceegister():
	if 'submit' in request.form:
		q="select max(user_id) as id from user"
		res=select(q)
		print(res)
		val=res[0]['id']
		print(val)
		image1=request.files['image1']
		image2=request.files['image2']
		image3=request.files['image3']
		image4=request.files['image4']
		# path = 'static/uploads/'
		path=""
		# Check whether the   
		# specified path is   
		# an existing file 
		isFile = os.path.isdir("static/uploads/"+str(val))  
		print(isFile)
		if(isFile==False):
			os.mkdir('static\\uploads\\'+str(val))
		path="static/uploads/"+str(val)+"/"+str(uuid.uuid4())+image1.filename
		image1.save(path)
		path="static/uploads/"+str(val)+"/"+str(uuid.uuid4())+image2.filename
		image2.save(path)
		path="static/uploads/"+str(val)+"/"+str(uuid.uuid4())+image3.filename
		image3.save(path)
		path1="static/checking/ocrfiles/fileocr.jpg"
		image4.save(path1)

		enf("static/uploads/")
		content=ocrgenerate(path1)
		print("gh",content)
		q="update `user` set ocrfile='%s' where user_id='%s'" %(content,str(val))
		print(q)
		update(q)
		return redirect(url_for('home'))

	return render_template('userfaceegister.html')



@app.route('/login_action/',methods=['get','post'])
def login_action():
	data = {}
	if 'login' in request.form:
		name=request.form['username']
		features=request.form['features']
		print(features)
		s="select * from login inner join `user`using(login_id) where username='%s'"%(name)
		sel=select(s)
		if len(sel)>0:
			bool = get_login_id(features)
			print("dsf",bool)
			if bool != 1: 
				session['login_id'] = sel[0]['login_id']
				session['user_id'] = sel[0]['user_id']
				session['ocrfile'] = sel[0]['ocrfile']
				data['status'] = 'success'
				data['data'] = sel
			else:
				data['status'] = 'failed'
				data['reason'] = 'Time difference'
		else:
			data['status'] = 'failed'
			data['reason'] = 'Username  is incorrect'
	return demjson.encode(data)

@app.route('/register_action/',methods=['get','post'])
def register_action():
	if 'register' in request.form:
		print("haiii")
		fnam=request.form['fname']
		lnam=request.form['lname']
		ag=request.form['age']
		eml=request.form['email']
		phn=request.form['phone']
		user=request.form['user']
		features=request.form['features']
		lo="insert into login(username,features,usertype)values('%s','%s','user')"%(user,features)
		log=insert(lo)
		q="insert into `user`(login_id,fname,lname,age,email,phone)values('%s','%s','%s','%s','%s','%s')"%(log,fnam,lnam,ag,eml,phn)
		res=insert(q)
		train()
		

		return "ok"


# @app.route('/startvideo/',methods=['get','post'])
# def startvideo():
# 	return render_template('startvideo.html')



app.run(debug=True,port=5002)