#Fareed 
from flask import Flask, g
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'helloworld'  # Set a secret key for the application
app.config['DATABASE'] = 'app.db'  # Set the database file name

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # Connect to the database if not already connected
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row  # Set the row factory to return rows as dictionary-like objects
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # Close the database connection when the application context is torn down
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            # Execute the SQL script to initialize the database schema
            db.cursor().executescript(f.read())
        db.commit()

# Comment out or remove the following lines to prevent automatic reinitialization
# with app.app_context():
#     init_db()

# Import routes and models modules from the app package
from app import routes, models