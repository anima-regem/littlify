from flask import Flask, render_template, request, redirect, Blueprint,url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' :
        try:
            u_email = request.form['email']
            if(email_validator(u_email)):
                u_password = request.form['password']
                user = User.objects.get(email=u_email)
                if(check_password_hash(user.password,u_password)):
                    login_user(user)
                    flash('Login Successful!', category='success')
                    return redirect(url_for('views.home'))
                else:
                    flash('Invalid Credentials!', category='error')
                    return redirect(url_for('auth.login'))
            else:
                flash('Invalid Email!',category='error')
                return redirect(url_for('auth.login'))
        except :
            flash('User Not Found!', category='success')
            return redirect(url_for('auth.login'))
    else:
        return render_template('login.html')

@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        try:
            u_email = request.form.get('email')
            if(email_validator(u_email)):    
                u_password = request.form.get('password')
                h_password = generate_password_hash(u_password)
                User.objects.create(email=u_email,password=h_password)
                flash('Sign Up Successful!',category='success')
                return redirect(url_for('auth.login'))
            else:
                flash('Invalid Email!',category='error')
                return redirect(url_for('auth.signup'))
        except NotUniqueError:
            flash("Email ALready Registered!", category='error')
            return redirect(url_for('auth.signup'))
    else:
        return render_template('signup.html')

@auth.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged Out Successfully!", category='success')
    return redirect(url_for('auth.login'))


def email_validator(mailid):
    if('@' in mailid) and ('.' in mailid) and len(mailid)>5:
        return True
    return False