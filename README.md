# udemy-advanced-restapi-flask-python
1. [Advanced REST APIs with Flask and Python](https://www.udemy.com/course/advanced-rest-apis-flask-python)
2. Used with Pylance extension to practice typed annotations with Python as well.
3. Install pipenv: `py -m pip install pipenv`
4. Create new pipenv project: `py -m pipenv --python 3.9`, temporary disable uwsgi and psycopg2 first
5. Update .vscode settings with virtualenv location
```
"python.analysis.extraPaths": [
    "C:\\Users\\Kaiser\\.virtualenvs\\udemy-advanced-restapi-flask-python-YiY2U8V4\\Lib\\site-packages",
],
```
6. Install dependencies: `py -m pipenv install --dev`
7. Run pipenv: `py -m pipenv shell`
8. Check pipenv dependencies: `py -m pipenv graph`
9. Exit pipenv: `exit`
10. Run black formatting: `black .`

# Production Only
1. `py -m pipenv install uwsgi`, `py -m pipenv install psycopg2`

# Troubleshooting pipenv
1. Restart VSCode and select pipenv intepreter
2. Remove virtual env: `py -m pipenv --rm`
3. Restart VSCode after installing dependencies

# Database migrations
1. Encrypting password [Encrypting passwords in Python with passlib](https://blog.teclado.com/learn-python-encrypting-passwords-python-flask-and-passlib/)
2. ElephantSQL - [ElephantSQL](elephantsql.com)
3. Copy instance url to env `SQLALCHEMY_DATABASE_URI`
4. For local: `pipenv install psycopg2-binary` to run postgres
5. ElephantSQL - Drop user table: `DROP TABLE users CASCADE`
6. Create migration folders: `py -m flask db init`. Make sure in app.py error
7. Upgrade migration: `py -m flask db upgrade`
8. After any schema update run migrate: `py -m flask db migrate -m <MSG>`. After changing the models py files directly.
9. Check current migration version: `SELECT * FROM alembic_version`
10. IMPORTANT: Make sure all contraints are named when creating migrations. (Set your own constraint names or set conventions in db.py)
Good to define own names to standardize across all different databases.

