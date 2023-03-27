from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from markupsafe import escape

app = Flask(__name__)

#flash pour les messages

@app.route('/login', methods=['POST', 'GET'])
def login(redirect=None):
    return f'Salut'
    # error = None
    # if request.method == 'POST':
    #     if valid_login(request.form['username'],
    #                    request.form['password']):
    #         return log_the_user_in(request.form['username'])
    #     else:
    #         error = 'Invalid username/password'
    # # the code below is executed if the request method
    # # was GET or the credentials were invalid
    # return render_template('login.html', error=error)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

def checkSession():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return redirect(url_for('login'))

@app.route('/')
def index():
    return checkSession()

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'

with app.test_request_context():
    print(url_for('hello', name='Camille'))
    print(url_for('index'))