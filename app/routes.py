from flask import render_template, request, redirect, url_for, flash, session
from app import app, get_db
from app.flight_api import search_flights_with_entity_ids
from app.flight_api import auto_complete
from app.models import get_favorites
from sqlite3 import Row

#Fareed
@app.route('/')
def index():
    # Render the index template
    return render_template('index.html')

#Fareed
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        db.row_factory = Row
        error = None
        # Query the database for the user with the provided username
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            error = 'Invalid username.'
        elif user['password'] != password:
            error = 'Invalid password.'
        if error is None:
            # Clear the session and store the user's ID
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    # Render the login template
    return render_template('login.html')

#Hisham
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        db.row_factory = Row
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            # Insert the new user into the database
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            db.commit()
            user = db.execute(
                'SELECT * FROM users WHERE username = ?', (username,)
            ).fetchone()
            if user:
                # Store the user's ID in the session
                session['user_id'] = user['id']
                return redirect(url_for('index'))

        flash(error)

    # Render the registration template
    return render_template('register.html')

#Hisham
@app.route('/logout')
def logout():
    # Remove the user's ID from the session
    session.pop('user_id', None)
    return redirect(url_for('index'))

#Hisham
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Get the search parameters from the form
        origin_query = request.form.get('origin')
        destination_query = request.form.get('destination')
        date = request.form.get('date')

        # Get the entity IDs for the origin and destination locations
        origin_entity_id = auto_complete(origin_query)
        destination_entity_id = auto_complete(destination_query)

        if not origin_entity_id:
            flash(f"Could not find a location matching '{origin_query}'. Please enter a valid departure location.")
            return render_template('search.html')  # Stop further execution if there's an error

        if not destination_entity_id:
            flash(f"Could not find a location matching '{destination_query}'. Please enter a valid arrival location.")
            return render_template('search.html')  # Stop further execution if there's an error

        # Search for flights based on the provided entity IDs and date
        flights = search_flights_with_entity_ids(origin_entity_id, destination_entity_id, date)
        if flights:
            return render_template('search_results.html', flights=flights, origin=origin_query, destination=destination_query)
        else:
            flash('No flights found for the provided search criteria. Please try again with different locations or dates.')
            return render_template('search.html')  # Stop further execution if there's an error

    # Render the search template
    return render_template('search.html')

#Alex
@app.route('/favorites')
def favorites():
    if 'user_id' in session:
        user_id = session['user_id']
        # Get the user's favorites
        favorites = get_favorites(user_id)
        return render_template('favorites.html', favorites=favorites)
    else:
        return redirect(url_for('login'))

#Fareed
@app.route('/aboutus')
def aboutus():
    # Render the about us template
    return render_template('aboutus.html')
    
#Alex
@app.route('/add_favorite/<int:flight_id>', methods=['POST'])
def add_favorite(flight_id):
    if 'user_id' not in session:
        flash('You must be logged in to add favorites.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = get_db()
    # Check if the favorite already exists
    existing_favorite = db.execute(
        'SELECT 1 FROM favorites WHERE user_id = ? AND flight_id = ?',
        (user_id, flight_id)
    ).fetchone()

    if existing_favorite:
        flash('This flight is already in your favorites.', 'warning')  #'warning' category for the message
    else:
        try:
            # Insert the new favorite into the database
            db.execute(
                'INSERT INTO favorites (user_id, flight_id) VALUES (?, ?)',
                (user_id, flight_id)
            )
            db.commit()
            flash('Flight added to favorites.', 'success')  #'success' category for a positive message
        except sqlite3.IntegrityError:
            flash('This flight is already in your favorites.', 'warning')

    return redirect(url_for('favorites'))