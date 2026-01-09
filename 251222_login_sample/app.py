from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret_key_example"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="MW81"   # ← DB名を指定
    )

@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT * FROM users
        WHERE user_id = %s AND password = %s
        """
        cursor.execute(sql, (user_id, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["user_id"] = user["user_id"]
            return redirect(url_for("dashboard"))
        else:
            error = "ユーザーIDまたはパスワードが間違っています"

    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return f"ログイン成功：{session['user_id']}"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
