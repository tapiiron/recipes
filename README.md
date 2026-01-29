# recipes
Recipes - HU school work web-software 2026

Requirements
+ Users can share their recipes. In the recipe there are needed incredients and cooking instructions with a picture
+ User can create a new user and login to the software
+ User can add, edit and remove recipes
+ User can see all recipes added
+ User can search recipes
- Userpage shows how many recipes user have added and list of own recipes
+ User can select recipe one or more tags like starter, indian or vegan
- User can give comments to recipes and grade them
- In a recipe you can see all comments and average rating

How to run program:
1) Prepare database.db (linux)
  - sqlite3 database.db < schema.sql
  - sqlite3 database.db < init.sql
  - If in windows seems like you need to run sqlite3.exe database.db and then copy paste schema + init into console
2) Prepare python virtual environment
  - Check venv initialization and activation from course documentation
3) Run program in venv
  - flask run
  - Open browser to http://localhost:5000



