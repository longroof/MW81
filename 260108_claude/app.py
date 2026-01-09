from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# データベース接続設定
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'shopping_site'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE stock > 0 ORDER BY created_at DESC")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', products=products)
    return "Database connection error", 500

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        if product:
            return render_template('product_detail.html', product=product)
        return "Product not found", 404
    return "Database connection error", 500

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if product and product['stock'] >= quantity:
            if 'cart' not in session:
                session['cart'] = {}
            
            cart = session['cart']
            product_id_str = str(product_id)
            
            if product_id_str in cart:
                cart[product_id_str]['quantity'] += quantity
            else:
                cart[product_id_str] = {
                    'name': product['name'],
                    'price': float(product['price']),
                    'quantity': quantity
                }
            
            session['cart'] = cart
            flash(f'{product["name"]}をカートに追加しました', 'success')
        else:
            flash('在庫が不足しています', 'error')
    
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    
    if 'cart' in session:
        for product_id, item in session['cart'].items():
            cart_items.append({
                'product_id': product_id,
                'name': item['name'],
                'price': item['price'],
                'quantity': item['quantity'],
                'subtotal': item['price'] * item['quantity']
            })
            total += item['price'] * item['quantity']
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        del session['cart'][product_id]
        session.modified = True
        flash('商品をカートから削除しました', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        email = request.form.get('email')
        address = request.form.get('address')
        
        if 'cart' not in session or not session['cart']:
            flash('カートが空です', 'error')
            return redirect(url_for('cart'))
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            # 注文の合計金額を計算
            total = sum(item['price'] * item['quantity'] for item in session['cart'].values())
            
            # 注文を作成
            cursor.execute(
                "INSERT INTO orders (customer_name, email, address, total_amount, status) VALUES (%s, %s, %s, %s, %s)",
                (customer_name, email, address, total, 'pending')
            )
            order_id = cursor.lastrowid
            
            # 注文詳細を作成
            for product_id, item in session['cart'].items():
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (order_id, int(product_id), item['quantity'], item['price'])
                )
                
                # 在庫を減らす
                cursor.execute(
                    "UPDATE products SET stock = stock - %s WHERE id = %s",
                    (item['quantity'], int(product_id))
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # カートをクリア
            session.pop('cart', None)
            
            flash('ご注文ありがとうございます!', 'success')
            return redirect(url_for('order_complete', order_id=order_id))
    
    return render_template('checkout.html')

@app.route('/order_complete/<int:order_id>')
def order_complete(order_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('order_complete.html', order=order)
    return "Database connection error", 500

if __name__ == '__main__':
    app.run(debug=True)