
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from decimal import Decimal, ROUND_HALF_UP

app = Flask(__name__)
app.secret_key = "change-me-in-production"  # 本番では必ず環境変数等で管理してください

# --- 商品マスタ（本来はDB） ---
PRODUCTS = {
    "p001": {"id": "p001", "name": "ワイヤレスマウス", "price": 2980, "description": "静音クリック・Bluetooth対応"},
    "p002": {"id": "p002", "name": "メカニカルキーボード", "price": 9980, "description": "打鍵感が気持ちいい青軸"},
    "p003": {"id": "p003", "name": "USB-Cハブ", "price": 3480, "description": "HDMI/USB-A/SD搭載"},
    "p004": {"id": "p004", "name": "ノートPCスタンド", "price": 2580, "description": "高さ調整・放熱設計"},
}

TAX_RATE = Decimal("0.10")  # 10%
SHIPPING_FEE = 500  # 一律送料（例）


# --- ユーティリティ ---
def money_round(value: Decimal) -> Decimal:
    """金額の四捨五入（円）"""
    return value.quantize(Decimal("1"), rounding=ROUND_HALF_UP)

def get_cart() -> dict:
    """
    カート構造:
      session["cart"] = {
         "p001": 2,
         "p003": 1,
      }
    """
    cart = session.get("cart")
    if cart is None:
        cart = {}
        session["cart"] = cart
    return cart

def build_cart_items(cart: dict):
    """カートの明細（商品情報付き）を組み立てる"""
    items = []
    subtotal = Decimal("0")

    for pid, qty in cart.items():
        product = PRODUCTS.get(pid)
        if not product:
            # 商品が消えていたらスキップ（必要なら削除してもよい）
            continue
        qty = int(qty)
        price = Decimal(str(product["price"]))
        line_total = price * qty
        subtotal += line_total
        items.append({
            "id": pid,
            "name": product["name"],
            "price": int(price),
            "qty": qty,
            "line_total": int(line_total),
        })

    tax = money_round(subtotal * TAX_RATE)
    shipping = Decimal(str(SHIPPING_FEE)) if subtotal > 0 else Decimal("0")
    total = subtotal + tax + shipping

    summary = {
        "subtotal": int(subtotal),
        "tax": int(tax),
        "shipping": int(shipping),
        "total": int(total),
    }
    return items, summary


# --- ルート ---
@app.route("/")
def index():
    cart = get_cart()
    cart_count = sum(int(q) for q in cart.values())
    return render_template("index.html", products=PRODUCTS.values(), cart_count=cart_count)

@app.route("/product/<product_id>")
def product_detail(product_id):
    product = PRODUCTS.get(product_id)
    if not product:
        abort(404)
    cart = get_cart()
    cart_count = sum(int(q) for q in cart.values())
    return render_template("product.html", product=product, cart_count=cart_count)

@app.route("/add_to_cart/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    if product_id not in PRODUCTS:
        abort(404)

    qty = request.form.get("qty", "1")
    try:
        qty = int(qty)
        if qty < 1:
            qty = 1
    except ValueError:
        qty = 1

    cart = get_cart()
    cart[product_id] = int(cart.get(product_id, 0)) + qty
    session["cart"] = cart

    flash("カートに追加しました。", "success")
    return redirect(url_for("cart_view"))

@app.route("/cart")
def cart_view():
    cart = get_cart()
    items, summary = build_cart_items(cart)
    cart_count = sum(int(q) for q in cart.values())
    return render_template("cart.html", items=items, summary=summary, cart_count=cart_count)

@app.route("/update_cart", methods=["POST"])
def update_cart():
    cart = get_cart()

    # quantities[product_id] = qty の形式で受け取る
    quantities = request.form.getlist("quantities[]")
    product_ids = request.form.getlist("product_ids[]")

    for pid, qty in zip(product_ids, quantities):
        if pid not in cart:
            continue
        try:
            q = int(qty)
        except ValueError:
            q = cart[pid]

        if q <= 0:
            cart.pop(pid, None)
        else:
            cart[pid] = q

    session["cart"] = cart
    flash("カートを更新しました。", "info")
    return redirect(url_for("cart_view"))

@app.route("/remove/<product_id>", methods=["POST"])
def remove_item(product_id):
    cart = get_cart()
    if product_id in cart:
        cart.pop(product_id, None)
        session["cart"] = cart
        flash("商品をカートから削除しました。", "info")
    return redirect(url_for("cart_view"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = get_cart()
    items, summary = build_cart_items(cart)
    cart_count = sum(int(q) for q in cart.values())

    if request.method == "GET":
        return render_template("checkout.html", items=items, summary=summary, cart_count=cart_count)

    # POST: 注文確定（簡易）
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    address = request.form.get("address", "").strip()

    if not items:
        flash("カートが空です。商品を追加してください。", "warning")
        return redirect(url_for("index"))

    if not name or not email or not address:
        flash("お届け先情報をすべて入力してください。", "danger")
        return render_template("checkout.html", items=items, summary=summary, cart_count=cart_count,
                               form={"name": name, "email": email, "address": address})

    # ここで本来はDB保存や決済処理などを行う
    order = {
        "name": name,
        "email": email,
        "address": address,
        "items": items,
        "summary": summary,
    }

    # カートを空にする
    session["cart"] = {}
    session["last_order"] = order

    flash("ご注文ありがとうございました！", "success")
    return redirect(url_for("complete"))

@app.route("/complete")
def complete():
    order = session.get("last_order")
    if not order:
        return redirect(url_for("index"))
    return render_template("complete.html", order=order, cart_count=0)

@app.errorhandler(404)
def not_found(e):
    return render_template("base.html", cart_count=sum(int(q) for q in get_cart().values()),
                           content_title="404 Not Found",
                           content_message="お探しのページは見つかりませんでした。"), 404

if __name__ == "__main__":
    app.run(debug=True)
