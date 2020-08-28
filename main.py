from flask import request, flash, url_for, make_response, session, redirect, render_template
import unittest
from flask_login import login_required, current_user
from app.forms import Login_Form, TodoForm
from app import create_app
from app.firestore_service import get_users, get_todos, todo_put

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
    email = current_user.email
    todo_form = TodoForm()
    context = {
        'todos': get_todos(username),
        'username': username,
        'email': email,
        'todo_form': todo_form,
    }

    if request.method == 'POST':
        todo_put(user_id=username, description=todo_form.description.data)
        flash('Task created', 'success')
        return redirect(url_for('hello'))
    return render_template('hello.html', **context)


if __name__ == '__main__':
    app.run(debug=False)