from flask import Flask, request, session, make_response, redirect, render_template, url_for, flash
import secrets
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = secrets.token_hex(20)

todos = ['1st todo', '2nd todo', '3rd todo']

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(505)
def not_supported(error):
    return render_template('404.html', error=error)

@app.route('/')
def index():
    ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = ip
    return response

@app.route('/hello', methods=['GET', 'POST'])
def Hello():
    ip = session.get('user_ip')
    username = session.get('username')
    login_form = LoginForm()
    context = {
        'user_ip': ip,
        'username': username,
        'todos': todos,
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('User registered correctly')

        return redirect(url_for('index'))

    return render_template('hello.html', **context)

@app.route('/goodbye')
def Bye():
    username = 'pal'
    if session.get('username') != None:
        username = session.get('username')
    context = {
        'message': f'Good bye, {username}.'
    }
    return render_template('bye.html', **context)

