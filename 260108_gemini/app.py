from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# データベース接続設定
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # 自分の環境に合わせて変更
        password="root", # 自分の環境に合わせて変更
        database="shop_gemini_db"
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('detail.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)