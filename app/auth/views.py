from flask import render_template, request, flash, url_for, session, redirect
from . import auth
from flask_login import login_user, logout_user
from app.forms import Login_Form
from app.firestore_service import get_user
from app.models import UserData, UserModel

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
            password_from_db = user_doc.to_dict()['password']
            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)
                flash('Bienvenido denuevo!','success')
                redirect(url_for('hello'))
            else:
                flash('Credenciales incorrectas','danger')
        else:
            flash('El usuario no existe', 'danger')

        return redirect(url_for('hello'))

    return render_template('auth/login.html', **context)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))