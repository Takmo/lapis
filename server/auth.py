# See LICENSE file in top directory!

import hashlib
import sqlite3

def connect_sqlite():
    return sqlite3.connect("db.sqlite")

def auth_user(db, username, password):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    if hash_password(password) == row[1]:
        return True
    return False

def create_user(db, username, password):
    # Verify that user does not already exist.
    for row in db.cursor().execute("SELECT * FROM users WHERE username=?", (username,)):
        print "User already exists!"
        return False
    # Add them to database.
    db.cursor().execute("INSERT INTO users (username, password, admin) " +
            "VALUES (?, ?, ?)", (username, hash_password(password), False))
    db.commit()
    return True

def hash_password(password):
    h = hashlib.sha512()
    h.update(password)
    out = h.hexdigest()
    h.update(password + out)
    return h.hexdigest()

def initialize_sqlite():
    c = connect_sqlite()
    c.cursor().execute("CREATE TABLE users (username VARCHAR(75), password VARCHAR(75), admin BOOLEAN)")
    c.close()

