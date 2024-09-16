from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
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
    cursor.execute('SELECT * FROM burgers')
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

#Köksvy: Visar order
@app.route('/kitchen')
def kitchen():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT orders.id, burgers.name, orders.quantity, orders.status, 
               GROUP_CONCAT(customizations.customization, ', ') as customizations 
        FROM orders 
        JOIN burgers ON orders.burger_id = burgers.id 
        LEFT JOIN customizations ON orders.id = customizations.order_id 
        WHERE orders.status = 'pending' 
        GROUP BY orders.id
    """)
    orders = cursor.fetchall()
    conn.close()
    return render_template('kitchenshow.html', orders=orders)

# Markera order som färdig
@app.route('/complete_order', methods=['POST'])
def complete_order():
    order_id = request.form.get('order_id')
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    
    return redirect('/kitchen')

#Aminvy för att lägga till, ändra och ta bort burgare
@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM burgers')
    burgers = cursor.fetchall()
    conn.close()
    return render_template('admin.html', burgers=burgers)

@app.route('/add_burger', methods=['POST'])
def add_burger():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    name = request.form.get('name')
    price = float(request.form.get('price'))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO burgers (name, price) VALUES (?, ?)', (name, price))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/edit_burger/<int:burger_id>', methods=['POST'])
def edit_burger(burger_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    name = request.form.get('name')
    price = float(request.form.get('price'))
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE burgers SET name = ?, price = ? WHERE id = ?', (name, price, burger_id))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/delete_burger/<int:burger_id>', methods=['POST'])
def delete_burger(burger_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM burgers WHERE id = ?', (burger_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

#Logga in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            return redirect(url_for('kitchen'))
        else:
            return 'Invalid credentials', 403
    return render_template('login.html')

#Logga ut
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('order_form'))


if __name__ == '__main__':
    app.run(debug=True)
