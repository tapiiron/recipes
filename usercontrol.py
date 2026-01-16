from werkzeug.security import generate_password_hash, check_password_hash

import db

def create_user(username,password):
    password_hash = generate_password_hash(password)
    sql = "select username from user where username=?"
    result = db.execute(sql, [username])
    if not result:
        sql = "insert into user (username,password_hash) values(?,?)"
        db.execute(sql, [username,password_hash])

def check_login(username,password):
    password_hash = generate_password_hash(password)
    sql = "select id from user where username=? and password_hash=?"
    result = db.query(sql, [username,password_hash])
    if not result:
        return None
    else:
        return result[0]["id"]

