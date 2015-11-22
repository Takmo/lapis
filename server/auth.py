# See LICENSE file in top directory!

import hashlib
import sqlite3

def connect_sqlite():
    return sqlite3.connect("db.sqlite")

def auth_user(db, username, password):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.rowcount is 0:
        print "User does not exist!"
        return False
    row = cursor.fetchone()
    if row is None:
        print "User does not exist!"
        return False
    if hash_password(password) == row[1]:
        return True
    return False

def create_user(db, username, password):
    # Verify that user does not already exist.
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.rowcount > 0:
        print "User already exists!"
        return False
    # Add them to database.
    cursor.execute("INSERT INTO users (username, password, admin) " +
            "VALUES (?, ?, ?)", (username, hash_password(password), False))
    db.commit()
    return True

def delete_user(db, username):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.rowcount is 0:
        print "User does not exist!"
        return False
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
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

def is_admin(db, username):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.rowcount is 0:
        print "User does not exist!"
        return False
    return (cursor.fetchone()[2] == 1)

def set_admin(db, username, flag=1):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.rowcount is 0:
        print "User does not exist!"
        return False
    cursor.execute("UPDATE users SET admin=? WHERE username=?", (flag, username))
    db.commit()
    return True

