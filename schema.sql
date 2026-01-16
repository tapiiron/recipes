create table user(
 id integer primary key autoincrement,
 username text name unique,
 password_hash text
);

create table recipe(
 id integer primary key autoincrement,
 id_user integer references user(id),
 name text,
 incredients text,
 instructions text,
 picture blob
);

create table tag(
 id integer primary key autoincrement,
 name text
);

create table recipe_tag(
 id_recipe integer references recipe(id),
 id_tag integer references tag(id)
);

create table recipe_comment(
 id_recipe integer references recipe(id),
 id_user integer references user(id),
 comment text,
 grade int
);

