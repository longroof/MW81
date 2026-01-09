from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# データベース接続設定
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'mw81_sample'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# ログイン必須デコレータ
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('ログインが必要です', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ログイン・登録関連
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            # ユーザー名とメールの重複チェック
            cursor.execute("SELECT * FROM t_users WHERE f_user_name = %s OR f_user_email = %s", (username, email))
            existing_user = cursor.fetchone()
            
            if existing_user:
                flash('ユーザー名またはメールアドレスが既に登録されています', 'error')
                cursor.close()
                conn.close()
                return render_template('register.html')
            
            # パスワードのハッシュ化
            password_hash = generate_password_hash(password)
            
            # ユーザーの登録
            cursor.execute(
                "INSERT INTO t_users (f_user_name, f_user_email, f_user_password_hash, f_user_full_name, f_user_address, f_user_phone) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, email, password_hash, full_name, address, phone)
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('登録が完了しました。ログインしてください', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM t_users WHERE f_user_name = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user and check_password_hash(user['f_user_password_hash'], password):
                session['user_id'] = user['f_user_id']
                session['username'] = user['f_user_name']
                session['full_name'] = user['f_user_full_name']
                flash(f'ようこそ、{user["f_user_full_name"]}さん!', 'success')
                return redirect(url_for('index'))
            else:
                flash('ユーザー名またはパスワードが正しくありません', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('ログアウトしました', 'success')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM t_users WHERE f_user_id = %s", (session['user_id'],))
        user = cursor.fetchone()
        
        # ユーザーの注文履歴を取得
        cursor.execute(
            "SELECT * FROM t_orders WHERE f_order_user_id = %s ORDER BY f_order_created_at DESC",
            (session['user_id'],)
        )
        orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return render_template('profile.html', user=user, orders=orders)
    return "Database connection error", 500

# 商品関連
@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM t_products WHERE f_product_stock > 0 ORDER BY f_product_created_at DESC")
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
        cursor.execute("SELECT * FROM t_products WHERE f_product_id = %s", (product_id,))
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
        cursor.execute("SELECT * FROM t_products WHERE f_product_id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if product and product['f_product_stock'] >= quantity:
            if 'cart' not in session:
                session['cart'] = {}
            
            cart = session['cart']
            product_id_str = str(product_id)
            
            if product_id_str in cart:
                cart[product_id_str]['quantity'] += quantity
            else:
                cart[product_id_str] = {
                    'name': product['f_product_name'],
                    'price': float(product['f_product_price']),
                    'quantity': quantity
                }
            
            session['cart'] = cart
            flash(f'{product["f_product_name"]}をカートに追加しました', 'success')
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
        # ログインユーザーの場合は情報を取得
        if 'user_id' in session:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM t_users WHERE f_user_id = %s", (session['user_id'],))
                user = cursor.fetchone()
                cursor.close()
                conn.close()
                
                customer_name = user['f_user_full_name']
                email = user['f_user_email']
                address = request.form.get('address') or user['f_user_address']
        else:
            customer_name = request.form.get('customer_name')
            email = request.form.get('email')
            address = request.form.get('address')
        
        if 'cart' not in session or not session['cart']:
            flash('カートが空です', 'error')
            return redirect(url_for('cart'))
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            total = sum(item['price'] * item['quantity'] for item in session['cart'].values())
            
            # 注文を作成
            user_id = session.get('user_id')
            cursor.execute(
                "INSERT INTO t_orders (f_order_user_id, f_order_customer_name, f_order_email, f_order_address, f_order_total_amount, f_order_status) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, customer_name, email, address, total, 'pending')
            )
            order_id = cursor.lastrowid
            
            # 注文詳細を作成
            for product_id, item in session['cart'].items():
                cursor.execute(
                    "INSERT INTO t_order_items (f_order_id, f_product_id, f_order_item_quantity, f_order_item_price) VALUES (%s, %s, %s, %s)",
                    (order_id, int(product_id), item['quantity'], item['price'])
                )
                
                cursor.execute(
                    "UPDATE t_products SET f_product_stock = f_product_stock - %s WHERE f_product_id = %s",
                    (item['quantity'], int(product_id))
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            session.pop('cart', None)
            
            flash('ご注文ありがとうございます!', 'success')
            return redirect(url_for('order_complete', order_id=order_id))
    
    # GET リクエストの場合
    user = None
    if 'user_id' in session:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM t_users WHERE f_user_id = %s", (session['user_id'],))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
    
    return render_template('checkout.html', user=user)

@app.route('/order_complete/<int:order_id>')
def order_complete(order_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM t_orders WHERE f_order_id = %s", (order_id,))
        order = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('order_complete.html', order=order)
    return "Database connection error", 500

if __name__ == '__main__':
    app.run(debug=True)