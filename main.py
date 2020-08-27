from flask import request, flash, url_for, make_response, session, redirect, render_template
import unittest
from flask_login import login_required, current_user
from app.forms import Login_Form
from app import create_app
from app.firestore_service import get_users, get_todos

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/error404.html', error=error)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    username = current_user.id
    
    context = {
        'todos': get_todos(username),
        'username': username,
    }
    users = get_users()
    for user in users:
        print(user.id)
        print(user.to_dict()['password'])
    return render_template('hello.html', **context)

if __name__ == '__main__':
    app.run(debug=True)