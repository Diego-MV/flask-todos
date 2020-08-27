from flask import render_template, request, flash, url_for, session, redirect
from . import auth
from flask_login import login_user, logout_user
from app.forms import Login_Form, Signup_Form
from app.firestore_service import get_user, user_put
from app.models import UserData, UserModel
from werkzeug.security import generate_password_hash, check_password_hash

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = Login_Form()
    context = {
        'login_form': login_form
    }

    if request.method == 'POST':
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)

        if user_doc.to_dict():
            if check_password_hash(user_doc.to_dict()['password'],password):
                email = user_doc.to_dict()['email']
                user_data = UserData(username, password, email)
                user = UserModel(user_data)

                login_user(user)
                flash('Welcome again!','success')
                redirect(url_for('hello'))
            else:
                flash('Username or password is incorrect','danger')
        else:
            flash('Username not found', 'danger')

        return redirect(url_for('hello'))

    return render_template('auth/login.html', **context)

@auth.route('/logout')
def logout():
    logout_user()
    flash('Come back soon !','success')
    return redirect(url_for('index'))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    signup_form = Signup_Form()
    context = {
        'signup_form': signup_form
    }
    if request.method == 'POST':
        username = signup_form.username.data
        email = signup_form.email.data
        password = signup_form.password.data
        
        user_doc = get_user(username)
        email_doc = get_user(email)

        if user_doc or email_doc is None:
            pass_hash = generate_password_hash(password)
            user_data = UserData(username, pass_hash, email)
            user_put(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Welcome', 'success')
            return redirect(url_for('hello'))
        else:
            flash('The user exist', 'danger')

    return render_template('auth/signup.html', **context)
   
@auth.route('/account')
def account():
    return render_template('auth/account.html')