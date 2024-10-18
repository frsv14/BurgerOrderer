import _mysql_connector

#skapar kontakt med databasen
conn = _mysql_connector.connect(
    host ='mysql',
    user ='root',
    password ='example',
    database ='burgerdb'
)
cursor = conn.cursor()

# Tar bort tabellerna om de redan finns
cursor.execute('DROP TABLE IF EXISTS customizations')
cursor.execute('DROP TABLE IF EXISTS orders')
cursor.execute('DROP TABLE IF EXISTS burgers')
cursor.execute('DROP TABLE IF EXISTS users')

# Skapar tabell för burgare
cursor.execute('''
CREATE TABLE IF NOT EXISTS burgers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2)
)
''')

# Skapar tabell för ordrar
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    burger_id INT,
    quantity INT,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(255),
    FOREIGN KEY (burger_id) REFERENCES burgers(id)
)
''')

# Skapar tabell för customizations
cursor.execute('''
CREATE TABLE IF NOT EXISTS customizations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    customization TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
)
''')

# Skapar tabell för användare
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
)
''')

#  lägger till några burgare
cursor.execute('INSERT IGNORE INTO burgers (name, description, price) VALUES ("OSTBURGARE", "", "120")')
cursor.execute('INSERT IGNORE INTO burgers (name, description, price) VALUES ("VEGGIEBURGARE", "", "100")')
cursor.execute('INSERT IGNORE INTO burgers (name, description, price) VALUES ("BACONBURGARE", "", "130")')

# Commit och stäng
conn.commit()
conn.close()
