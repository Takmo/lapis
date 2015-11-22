# See LICENSE file in top directory!

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash, redirect
from auth import auth_user, connect_sqlite
from server import Server

from uuid import uuid4

UPLOAD_FOLDER = '/path/to/uploads'
ALLOWED_EXTENSIONS = set(['.publishsettings'])

# The Flask app we'll be using.
app = Flask(__name__)
server = Server()

# Load default config and override config from an environment variable
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(dict(
    DEBUG=False,
    SECRET_KEY=os.urandom(24), 
))

@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        con = connect_sqlite()
        if not auth_user(con, username, password):
            return redirect("/static/login.html?fail=1")
        else:
            token = uuid4()
            session["token"] = token
            server.insert_token(token, username)
            return redirect("/")
    return redirect("/static/login.html")

@app.route("/logout")
def logout():
    session.pop("token", None)
    return redirect("/static/login.html")

@app.route("/status")
def status():
    if server.online:
        return "ONLINE"
    return "OFFLINE"

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
    return redirect("/static/login.html")

if __name__ == '__main__':
    app.run(debug=True)
