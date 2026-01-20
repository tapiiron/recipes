import db

# Lists recipies (for front page)
def list_recipies():
    result = db.query("select id,name from recipe")
    if not result:
        return None
    else:
        return result

