import sqlite3

# Replace 'your_database.db' with the path to actual database file
database_file = r'C:\xampp\htdocs\flight_locator\app.db'

def view_users(cursor):
    print("Users:")
    print("{:<20} {}".format("Username", "Password"))
    print("-" * 40)
    cursor.execute("SELECT username, password FROM users")
    users = cursor.fetchall()
    for username, password in users:
        print("{:<20} {}".format(username, password))
    print("\n")

def view_favorites(cursor):
    print("Favorites:")
    print("{:<20} {}".format("Username", "Flight ID"))
    print("-" * 40)
    # Adjust the following SQL query if your table or column names are different
    cursor.execute("""
        SELECT users.username, favorites.flight_id
        FROM favorites
        INNER JOIN users ON users.id = favorites.user_id
    """)
    favorites = cursor.fetchall()
    for username, flight_id in favorites:
        print("{:<20} {}".format(username, flight_id))
    print("\n")



def view_database(database_file):
    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    # View users
    view_users(cursor)
    
    # View favorites
    view_favorites(cursor)

    # Close the connection to the database
    conn.close()


if __name__ == "__main__":
    view_database(database_file)
