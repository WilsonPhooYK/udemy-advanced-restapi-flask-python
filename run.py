from app import app
from db import db
from ma import ma

db.init_app(app)
ma.init_app(app)
# Run method before first request into app
# NEED TO IMPORT ALL MODELS SO DB CAN CREATE TABLE
@app.before_first_request
def create_tables():
    db.create_all()
