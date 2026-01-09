from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import pooling
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "CHANGE_ME_TO_RANDOM_SECRET"

# ===== DB設定（必要に応じて環境変数化してください） =====
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "root",
    "database": "shop_db",
    "port": 3306,
    "charset": "utf8mb4",
    # "collation": "utf8mb4_0900_ai_ci",
}

cnx_pool = pooling.MySQLConnectionPool(
    pool_name="shop_pool",
    pool_size=5,
    **DB_CONFIG
)

def get_conn():
    return cnx_pool.get_connection()

def fetchone(query, params=None):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        row = cur.fetchone()
        cur.close()
        return row
    finally:
        conn.close()

def fetchall(query, params=None):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows
    finally:
        conn.close()

def execute(query, params=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(query, params or ())
        conn.commit()
        last_id = cur.lastrowid
        cur.close()
        return last_id
    finally:
        conn.close()

def login_required():
    if "user_id" not in session:
        flash("ログインが必要です。", "warning")
        return False
    return True

# ===== カート（セッション）ユーティリティ =====
def get_cart():
    # cart: {product_id(str): quantity(int)}
    return session.setdefault("cart", {})

def cart_count():
    cart = get_cart()
    return sum(cart.values())

def cart_items_with_products():
    cart = get_cart()
    if not cart:
        return []

    product_ids = [int(pid) for pid in cart.keys()]
    placeholders = ",".join(["%s"] * len(product_ids))
    products = fetchall(
        f"SELECT id, name, price, stock, image_url FROM products WHERE id IN ({placeholders}) AND is_active=1",
        product_ids
    )
    prod_map = {p["id"]: p for p in products}

    items = []
    for pid_str, qty in cart.items():
        pid = int(pid_str)
        p = prod_map.get(pid)
        if not p:
            continue
        line_total = p["price"] * qty
        items.append({
            "product": p,
            "quantity": qty,
            "line_total": line_total
        })
    return items

def cart_total_amount(items):
    return sum(i["line_total"] for i in items)

@app.context_processor
def inject_globals():
    return {
        "cart_count": cart_count(),
        "current_user": get_current_user()
    }

def get_current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return fetchone("SELECT id, email, name FROM users WHERE id=%s", (uid,))

# ===== ルーティング =====
@app.get("/")
def index():
    products = fetchall(
        "SELECT id, name, price, stock, image_url FROM products WHERE is_active=1 ORDER BY created_at DESC"
    )
    return render_template("index.html", products=products)

@app.get("/product/<int:product_id>")
def product_detail(product_id):
    product = fetchone(
        "SELECT id, name, description, price, stock, image_url FROM products WHERE id=%s AND is_active=1",
        (product_id,)
    )
    if not product:
        abort(404)
    return render_template("product.html", product=product)

@app.post("/cart/add")
def cart_add():
    product_id = request.form.get("product_id", type=int)
    qty = request.form.get("quantity", type=int, default=1)
    if not product_id or qty <= 0:
        flash("不正な入力です。", "danger")
        return redirect(url_for("index"))

    product = fetchone("SELECT id, stock, is_active FROM products WHERE id=%s", (product_id,))
    if not product or product["is_active"] != 1:
        flash("商品が見つかりません。", "danger")
        return redirect(url_for("index"))

    cart = get_cart()
    current_qty = cart.get(str(product_id), 0)
    new_qty = current_qty + qty

    if new_qty > product["stock"]:
        flash("在庫数を超えています。", "warning")
        return redirect(url_for("product_detail", product_id=product_id))

    cart[str(product_id)] = new_qty
    session["cart"] = cart
    flash("カートに追加しました。", "success")
    return redirect(url_for("cart_view"))

@app.get("/cart")
def cart_view():
    items = cart_items_with_products()
    total = cart_total_amount(items)
    return render_template("cart.html", items=items, total=total)

@app.post("/cart/update")
def cart_update():
    cart = get_cart()

    # quantities[product_id] = quantity
    for key, value in request.form.items():
        if not key.startswith("qty_"):
            continue
        pid_str = key.replace("qty_", "")
        qty = int(value) if value.isdigit() else 0

        if qty <= 0:
            cart.pop(pid_str, None)
        else:
            product = fetchone("SELECT stock, is_active FROM products WHERE id=%s", (int(pid_str),))
            if not product or product["is_active"] != 1:
                cart.pop(pid_str, None)
                continue
            if qty > product["stock"]:
                qty = product["stock"]
                flash("在庫数に合わせて数量を調整しました。", "info")
            cart[pid_str] = qty

    session["cart"] = cart
    flash("カートを更新しました。", "success")
    return redirect(url_for("cart_view"))

@app.post("/cart/clear")
def cart_clear():
    session["cart"] = {}
    flash("カートを空にしました。", "info")
    return redirect(url_for("cart_view"))

@app.get("/checkout")
def checkout():
    if not login_required():
        return redirect(url_for("login", next=url_for("checkout")))

    items = cart_items_with_products()
    if not items:
        flash("カートが空です。", "warning")
        return redirect(url_for("index"))

    total = cart_total_amount(items)
    return render_template("checkout.html", items=items, total=total)

@app.post("/checkout")
def checkout_post():
    if not login_required():
        return redirect(url_for("login", next=url_for("checkout")))

    items = cart_items_with_products()
    if not items:
        flash("カートが空です。", "warning")
        return redirect(url_for("index"))

    user_id = session["user_id"]

    conn = get_conn()
    try:
        conn.start_transaction()
        cur = conn.cursor(dictionary=True)

        # 在庫チェック（SELECT ... FOR UPDATE でロック）
        for item in items:
            pid = item["product"]["id"]
            cur.execute("SELECT stock, is_active, name, price FROM products WHERE id=%s FOR UPDATE", (pid,))
            row = cur.fetchone()
            if not row or row["is_active"] != 1:
                raise ValueError("商品が無効です。")
            if item["quantity"] > row["stock"]:
                raise ValueError(f"在庫不足: {row['name']}")

        total_amount = sum(item["line_total"] for item in items)

        # orders 作成
        cur.execute(
            "INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s)",
            (user_id, total_amount, "PAID")
        )
        order_id = cur.lastrowid

        # 明細 + 在庫減算
        for item in items:
            p = item["product"]
            qty = item["quantity"]
            line_total = item["line_total"]

            # 注文時点の名称/単価を保存
            cur.execute(
                """INSERT INTO order_items
                   (order_id, product_id, product_name, unit_price, quantity, line_total)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (order_id, p["id"], p["name"], p["price"], qty, line_total)
            )

            cur.execute(
                "UPDATE products SET stock = stock - %s WHERE id=%s",
                (qty, p["id"])
            )

        conn.commit()

        session["cart"] = {}
        flash("注文が完了しました！", "success")
        return redirect(url_for("order_complete", order_id=order_id))

    except Exception as e:
        conn.rollback()
        flash(f"注文処理に失敗しました: {e}", "danger")
        return redirect(url_for("checkout"))
    finally:
        conn.close()

@app.get("/order/complete/<int:order_id>")
def order_complete(order_id):
    if not login_required():
        return redirect(url_for("login"))

    order = fetchone("SELECT * FROM orders WHERE id=%s AND user_id=%s", (order_id, session["user_id"]))
    if not order:
        abort(404)

    items = fetchall("SELECT * FROM order_items WHERE order_id=%s", (order_id,))
    return render_template("order_complete.html", order=order, items=items)

@app.get("/orders")
def my_orders():
    if not login_required():
        return redirect(url_for("login"))

    orders = fetchall(
        "SELECT id, total_amount, status, created_at FROM orders WHERE user_id=%s ORDER BY created_at DESC",
        (session["user_id"],)
    )
    return render_template("my_orders.html", orders=orders)

# ===== 認証 =====
@app.get("/register")
def register():
    return render_template("register.html")

@app.post("/register")
def register_post():
    email = request.form.get("email", "").strip().lower()
    name = request.form.get("name", "").strip()
    password = request.form.get("password", "")

    if not email or not name or not password:
        flash("すべての項目を入力してください。", "warning")
        return redirect(url_for("register"))

    exists = fetchone("SELECT id FROM users WHERE email=%s", (email,))
    if exists:
        flash("そのメールアドレスは既に登録されています。", "danger")
        return redirect(url_for("register"))

    pw_hash = generate_password_hash(password)
    user_id = execute(
        "INSERT INTO users (email, password_hash, name) VALUES (%s, %s, %s)",
        (email, pw_hash, name)
    )

    session["user_id"] = user_id
    flash("登録が完了しました。", "success")
    return redirect(url_for("index"))

@app.get("/login")
def login():
    return render_template("login.html", next=request.args.get("next", ""))

@app.post("/login")
def login_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    next_url = request.form.get("next", "")

    user = fetchone("SELECT id, email, password_hash, name FROM users WHERE email=%s", (email,))
    if not user or not check_password_hash(user["password_hash"], password):
        flash("メールアドレスまたはパスワードが違います。", "danger")
        return redirect(url_for("login"))

    session["user_id"] = user["id"]
    flash(f"ようこそ {user['name']} さん", "success")
    return redirect(next_url or url_for("index"))

@app.get("/logout")
def logout():
    session.clear()
    flash("ログアウトしました。", "info")
    return redirect(url_for("index"))

# ===== エラーハンドリング =====
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
