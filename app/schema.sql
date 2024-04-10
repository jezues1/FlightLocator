--Hisham

-- Check if the 'users' table exists and drop it if it does to prevent errors on creation
DROP TABLE IF EXISTS users;
-- Check if the 'favorites' table exists and drop it if it does to prevent errors on creation
DROP TABLE IF EXISTS favorites;

-- Create a new 'users' table to store user information
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- A unique ID for each user, automatically incrementing
    username TEXT UNIQUE NOT NULL, -- The username must be unique and not null
    password TEXT NOT NULL -- The password must not be null
);

-- Create a new 'favorites' table to store user's favorite flights
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- A unique ID for each favorite, automatically incrementing
    user_id INTEGER NOT NULL, -- The ID of the user who favorited the flight, must not be null
    flight_id INTEGER NOT NULL, -- The ID of the flight that was favorited, must not be null
    FOREIGN KEY (user_id) REFERENCES users(id), -- Establish a foreign key relationship to the 'users' table
    UNIQUE (user_id, flight_id) -- Ensure each combination of user and flight is unique
);
