from flask import Flask, render_template, request, redirect, Blueprint,url_for, jsonify,flash
from flask_login import login_required, current_user
from .models import Data
import string
import secrets
from functools import reduce

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@views.route('/home/', methods=['GET','POST'])
@login_required
def home():
	if request.method =='POST':
		try:
			u_url = request.form['url']
			if(url_validator(u_url)):	
				li = list(map(lambda x: secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase), ['','','','','','','']))
				u_short = str(reduce((lambda x,y:x+y),li))
				Data.objects.create(short=u_short,url=u_url,owner=current_user.id)
				flash('URL Created!', category='success')
				return redirect(url_for('views.home'))
			else:
				flash('Enter a Valid URL', category='error')
				return redirect(url_for('views.home'))
		except :
			flash('Try Again!', category='error')
			return redirect(url_for('views.home'))
	else:
		return render_template('index.html')


@views.route('/<short>/', methods=['GET'])
def shortener(short):
	try:
		data = Data.objects.get(short=short)
		n_url = 'http://'+data.url
		return redirect(n_url)
	except:
		flash('URL Not Found!', category='error')
		return redirect(url_for('auth.login'))

@views.route('/urls/', methods=['GET'])
def urls():
	return render_template('admin.html', urls=Data.objects(owner=current_user.id))

def url_validator(url):
	if ('.' in url) and len(url)>3:
		return True
	return False

