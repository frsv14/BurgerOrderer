import sqlite3

#skapar kontakt med databasen
conn = sqlite3.connect('burgers.db')
cursor = conn.cursor()

# Tar bort tabellerna om de redan finns
cursor.execute('DROP TABLE IF EXISTS customizations')
cursor.execute('DROP TABLE IF EXISTS orders')
cursor.execute('DROP TABLE IF EXISTS burgers')

# Skapar tabell för burgare
cursor.execute('''
CREATE TABLE IF NOT EXISTS burgers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL
)
''')

# Skapar tabell för ordrar
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    burger_id INTEGER,
    quantity INTEGER,
    order_time TEXT,
    status TEXT,
    FOREIGN KEY (burger_id) REFERENCES burgers(id)
)
''')

# Skapar tabell för customizations
cursor.execute('''
CREATE TABLE IF NOT EXISTS customizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    customization TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
)
''')

# Skapar tabell för användare
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

#  lägger till några burgare
cursor.execute('INSERT OR IGNORE INTO burgers (name, description, price) VALUES ("OSTBURGARE", "", 120)')
cursor.execute('INSERT OR IGNORE INTO burgers (name, description, price) VALUES ("VEGGIEBURGARE", "", 100)')
cursor.execute('INSERT OR IGNORE INTO burgers (name, description, price) VALUES ("BACONBURGARE", "", 130)')

# Commit och stäng
conn.commit()
conn.close()
