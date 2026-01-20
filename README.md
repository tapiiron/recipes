# recipes
Recipes - HU school work web-software 2026

Requirements
- Users can share their recipes. In the recipe there are needed incredients and cooking instructions
- User can create a new user and login to the software
- User can add, edit and remove recipes
- User can see all recipes added
- User can search recipes
- Userpage shows how many recipes user have added and list of own recipes
- User can select recipe one or more classifications like starter, indian or vegan
- User can give comments to recipes and grade them
- In a recipe you can see all comments and average rating

Database structure
user
 - id pk
 - name
 - hashed password

recipe
 - id pk
 - id_user fk user
 - name
 - incredients
 - instructions
 - picture

tag
- id
- name

recipe_tag
 - id_recipe fk recipe
 - id_tag fk tag

recipe_comment
 - id_recipe fk recipe
 - id_user fk user
 - comment
 - grade

