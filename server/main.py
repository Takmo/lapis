# See LICENSE file in top directory!

import os
import uuid
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'lapis.db'),
    DEBUG=False,
    SECRET_KEY=os.urandom(24),
))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not auth_user(username, password):
            error = 'Invalid username or password'
        else:
            session['token'] = uuid4()
            flash('You were logged in')
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('token', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/')
def main():
    
