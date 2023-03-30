from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from pathlib import Path
from markupsafe import escape
import logging
import sqlite3
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

#flash pour les messages

def get_db():
    return sqlite3.connect('db.sqlite')

if not Path('db.sqlite').exists():
    db = get_db()
    sql = Path('db.sql').read_text()
    db.executescript(sql)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        if register_user(request.form['username'],
                       request.form['password'],
                       request.form['email']):
            return redirect(url_for('index'))
        else:
            error = 'Registration failed'
    # the code below is executed if the request method
    # was GET or the registration failed
    return render_template('register.html', error=error)

def valid_login(username, password):
    db = get_db()
    result = db.execute('SELECT password FROM users WHERE username = ?', [username])
    row = result.fetchone()
    if row is not None and row[0] == password:
        return True
    else:
        return False

def register_user(username, password, email):
    db = get_db()
    try:
        db.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', [username, password, email])
        db.commit()
        db.close()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        db.close()
        return False

def checkSession():
    if 'username' not in session:
        return 'not connected'
    return None

@app.route('/')
def index():
    error = checkSession()
    if error != None:
        return redirect(url_for('login'))
    return render_template('index.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

with app.test_request_context():
    print(url_for('index'))
