import db

# Lists recipies (for front page)
def list_recipes():
    result = db.query("select id,id_user,name,(select username from user where id = id_user) owner from recipe")
    if not result:
        return None
    else:
        return result

def list_recipes_by_user(id_user):
    result = db.query("select id,id_user,name from recipe where id_user=?",[id_user])
    if not result:
        return None
    else:
        return result

def show_user_recipe_statistics(id_user):
    result = db.query("select 'own_recipe_count' stat_name, count(*) stat_value from recipe where id_user=? "+
    "union select 'own_avg_rating' stat_name,ifnull(avg(rc.grade),0) stat_value from recipe r, recipe_comment rc where r.id_user=? and r.id = rc.id_recipe and rc.grade is not null "+
    "union select 'own_comments' stat_name,count(*) from recipe_comment where id_user=? "+
    "union select 'comments_on_own_recipies' stat_name, count(*) from recipe_comment rc, recipe r where r.id_user=? and r.id = rc.id_recipe"
    ,[id_user,id_user,id_user,id_user])
    if not result:
        return None
    else:
        return result    


def search_recipes(search,tag):
    query="select id,id_user,name,(select username from user where id = id_user) owner from recipe where (lower(name) like ? or lower(ingredients) like ? or lower(instructions) like ?)"
    params=['%'+search+'%','%'+search+'%','%'+search+'%']
    if tag:
        query += " and id in (select id_recipe from recipe_tag where id_tag=?)"
        params.append(tag)
    result = db.query(query,params)
    if not result:
        return None
    else:
        return result

def load_recipe(id):
    result = db.query("select id,id_user,name,ingredients,instructions,picture,(select username from user where id = id_user) owner from recipe r where r.id=?",[id])
    if not result:
        return None
    else:
        return result

def load_recipe_tags(id):
    result = db.query("select t.name from recipe_tag rt, tag t where rt.id_recipe=? and rt.id_tag=t.id",[id])
    if not result:
        return None
    else:
        return result

def list_recipe_tag_ids(id):
    result = db.query("select ''||id_tag id from recipe_tag where id_recipe=?",[id])
    if not result:
        return None
    else:
        return result

def list_tags():
    result = db.query("select ''||id id,name from tag order by name")
    if not result:
        return None
    else:
        return result

def add_recipe(id_user,name,ingredients,instructions,tags):
    db.execute("insert into recipe(id_user,name,ingredients,instructions) values (?,?,?,?)", 
               [id_user,name,ingredients,instructions])
    result = db.query("select max(id) maxid from recipe")
    inserted_id= result[0]["maxid"]
    for tag in tags:
        db.execute("insert into recipe_tag(id_recipe,id_tag) values (?,?)",[inserted_id,tag])

def update_recipe(id,name,ingredients,instructions,tags):
    db.execute("delete from recipe_tag where id_recipe=?",[id])
    for tag in tags:
        db.execute("insert into recipe_tag(id_recipe,id_tag) values (?,?)",[id,tag])
    db.execute("update recipe set name=?,ingredients=?,instructions=? where id=?",[name,ingredients,instructions,id])

def remove_recipe(id):
    db.execute("delete from recipe_comment where id_recipe=?",[id])
    db.execute("delete from recipe_tag where id_recipe=?",[id])
    db.execute("delete from recipe where id=?",[id])

def get_image(id):
    result = db.query("select picture from recipe where id=?",[id])
    return result[0]["picture"]

def update_picture(id,picture):
    db.execute("update recipe set picture=? where id=?",[picture,id])

def add_comment(id_recipe,id_user,comment,grade):
    db.execute("insert into recipe_comment(id_recipe,id_user,comment,grade) values(?,?,?,?)",[id_recipe,id_user,comment,grade])

def get_comments(id_recipe):
    return db.query("select rc.id,rc.id_recipe,rc.id_user,u.username,rc.comment,rc.grade,ifnull((select avg(grade) from recipe_comment rin where rin.id_recipe=rc.id_recipe),0) average from recipe_comment rc, user u " \
    "where rc.id_user=u.id and rc.id_recipe=?",[id_recipe])

def get_comment(id):
    return db.query("select id,id_recipe,id_user,comment,grade from recipe_comment where id=?",[id])

def delete_comment(id):
    db.execute("delete from recipe_comment where id=?",[id])
