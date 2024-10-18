from flask import Flask,flash , render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

#Ansluter till databasen    
def connect_db():
    conn = mysql.connector.connect(
        host='mysql',
        user='root',
        password='password',
        database='burgerdb'
    )
    return conn

#Köksvy: Visar order
@app.route('/')
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
    cursor.execute("UPDATE orders SET status = 'completed' WHERE id = %s", (order_id,))
    conn.commit()
    conn.close()
    
    return redirect('/')

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
    price = request.form.get('price')
    description = request.form.get('description')
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO burgers (name, description, price) VALUES (%s, %s, %s)', (name, description, price))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/edit_burger/<int:burger_id>', methods=['POST'])
def edit_burger(burger_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = connect_db()
    cursor = conn.cursor()

    name = request.form.get('name')
    price = request.form.get('price')
    description =request.form.get('description')

    try:
        float(price)
    except ValueError:
        flash('Price not a recogniced number!', 'warning')
    except TypeError:
        flash('Prise not a number', 'warning')
    else :    
        if price != '':
            cursor.execute('UPDATE burgers SET price = %s WHERE id = %s', (price, burger_id))


    if name != '':
        cursor.execute('UPDATE burgers SET name = %s WHERE id = %s', (name, burger_id) )

    if description != '' :
        cursor.execute('UPDATE burgers SET description = %s WHERE id = %s', (description, burger_id))

    if name != '' and price != '' and description != '':
        cursor.execute('UPDATE burgers SET name = %s, description = %s, price = %s WHERE id = %s', (name, description, price, burger_id))

    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/delete_burger/<int:burger_id>', methods=['POST'])
def delete_burger(burger_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM burgers WHERE id = %s', (burger_id,))
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
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
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
