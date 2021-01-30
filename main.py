from flask import Flask, request, make_response, redirect, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

todos = ['1st todo', '2nd todo', '3rd todo']

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
    response.set_cookie('user_ip', ip)
    return response

@app.route('/hello')
def Hello():
    ip = request.cookies.get('user_ip')
    context = {
        'user_ip': ip,
        'todos': todos
    }
    return render_template('hello.html', **context)

@app.route('/goodbye')
def Bye():
    context = {
        'message': 'Good bye, pal.'
    }
    return render_template('bye.html', **context)

