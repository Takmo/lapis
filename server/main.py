# See LICENSE file in top directory!

import os
from uuid import uuid4
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory
from azure import auth_user

UPLOAD_FOLDER = '/path/to/uploads'
ALLOWED_EXTENSIONS = set(['.publishsettings'])

# create our little application :)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            return redirect(url_for('upload'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('token', None)
    flash('You were logged out')
    return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('upload.html', error='Upload failed')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return redirect(url_for('main'))

@app.route('/', methods=['GET', 'POST'])
def main():
    # do stuff
    print "blah"
