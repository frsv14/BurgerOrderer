import sqlite3
from werkzeug.security import generate_password_hash

# Connect to the database
conn = sqlite3.connect('burgers.db')
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# User details
username = 'admin'
password = 'password123'  # Replace with a strong password

# Hash the password
hashed_password = generate_password_hash(password)

# Insert the user into the database
cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
conn.commit()

# Close the connection
conn.close()

print("User added successfully.")