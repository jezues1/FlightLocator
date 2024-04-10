# Hisham
from app import get_db

def get_user(user_id):
    # Get the database connection
    db = get_db()
    
    # Execute a SELECT query to retrieve the user with the specified user_id
    user = db.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    
    # Return the user object
    return user

def get_favorites(user_id):
    # Get the database connection
    db = get_db()
    
    # Execute a SELECT query to retrieve all favorites for the specified user_id
    favorites = db.execute(
        'SELECT * FROM favorites WHERE user_id = ?',
        (user_id,)
    ).fetchall()
    
    # Return the list of favorites
    return favorites