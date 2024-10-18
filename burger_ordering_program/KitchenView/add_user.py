import mysql.connector
from werkzeug.security import generate_password_hash

def connect_db():
    conn = mysql.connector.connect(
        host='mysql',
        user='root',
        password='password',
        database='burgerdb'
    )
    return conn

def add_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_user('admin', 'password')