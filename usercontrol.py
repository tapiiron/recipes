from werkzeug.security import check_password_hash,generate_password_hash

import db

def create_user(username,password):
    password_hash = generate_password_hash(password)
    sql = "select username from user where username=?"
    result = db.execute(sql, [username])
    if not result:
        sql = "insert into user (username,password_hash) values(?,?)"
        db.execute(sql, [username,password_hash])

def check_login(username,password):
    sql = "select id,password_hash from user where username=?"
    result = db.query(sql, [username])
    if not result:
        return None
    else:
        if check_password_hash(result[0]["password_hash"],password):
            return result[0]["id"]
        else:
            return None

