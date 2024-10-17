from flask import Flask, render_template, request
import sqlite3    
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

#Ansluter till databasen    
def connect_db():

    conn = sqlite3.connect('burgers.db')
    return conn

#Hemskärm: Visar order
@app.route('/')
def order_form():
    conn = connect_db() 
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM burgers')
    except sqlite3.OperationalError:
        exec('database.py')
        exec('add_burger.py')
    finally:
        burgers = cursor.fetchall()
        conn.close()
        return render_template('ordersite.html', burgers=burgers)
    
#Hantera burger-order
@app.route('/place_order', methods=['POST'])
def place_order():
    burger_id = request.form.get('burger_id')
    quantity = request.form.get('quantity')
    customizations = request.form.getlist('customizations')  
    custom_customizations = request.form.get('custom_customizations')
    
    # Skapar order i databasen
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (burger_id, quantity, order_time, status) VALUES (?, ?, ?, ?)', (burger_id, quantity, datetime.now(), "pending"))
    order_id = cursor.lastrowid  
    conn.commit()
    
    # Skapar customizations i databasen
    for customization in customizations:
        cursor.execute('INSERT INTO customizations (order_id, customization) VALUES (?, ?)', (order_id, customization))
    conn.commit()
    
    #Lägger till unika customizations i databasen
    if custom_customizations:
        cursor.execute('INSERT INTO customizations (order_id, customization) VALUES (?, ?)', (order_id, custom_customizations))
    
    conn.commit()
    
    # Hämtar information till orderbekräftelsen
    cursor.execute("SELECT name, price FROM burgers WHERE id = ?", (burger_id,))
    burger = cursor.fetchone()

    if not burger or not burger[1]:
        return 'Invalid burger', 400
   
    # Kalkylerar totalpris
    try:
        total_price = float(burger[1]) * int(quantity)
    except ValueError:
        conn.close()
        return "error: invalid price data" , 400

    # Stänger anslutning till databasen
    conn.close()
   
    # Skickar till orderbekräftelse
    return render_template('orderconfirmation.html', burger_name=burger[0], quantity=quantity, total_price=total_price)


if __name__ == '__main__':
    app.run(debug=True)
