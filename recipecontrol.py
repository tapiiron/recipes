import db

# Lists recipies (for front page)
def list_recipies():
    result = db.query("select id,id_user,name from recipe")
    if not result:
        return None
    else:
        return result

def load_recipe(id):
    result = db.query("select id,id_user,name,incredients,instructions,picture,group_concat((select id_tag from recipe_tag where id_recipe=r.id)) tags " \
    "from recipe r where r.id=?",[id])
    if not result:
        return None
    else:
        return result
    
def list_recipe_tags(id):
    result = db.query("select id,name,(select count(*) from recipe_tag where id_tag=t.id and id_recipe=?) selected from tags t",[id])
    if not result:
        return None
    else:
        return result

def list_tags():
    result = db.query("select id,name from tag order by name")
    if not result:
        return None
    else:
        return result

def add_recipe(id_user,name,incredients,instructions,tags):
    db.execute("insert into recipe(id_user,name,incredients,instructions) values (?,?,?,?)", 
               [id_user,name,incredients,instructions])
    result = db.query("select max(id) maxid from recipe")
    inserted_id= result[0]["maxid"]
    for tag in tags:
        db.execute("insert into recipe_tag(id_recipe,id_tag) values (?,?)",[inserted_id,tag])

def update_recipe(id,name,incredients,instructions):
    db.execute("update recipe set name=?,incredients=?,instructions=? where id=?",[name,incredients,instructions,id])

def get_image(id):
    result = db.query("select picture from recipe where id=?",[id])
    return result[0]["picture"]

def update_picture(id,picture):
    db.execute("update recipe set picture=? where id=?",[picture,id])