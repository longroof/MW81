from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flaskアプリのインスタンスを作成
app = Flask(__name__)

# MySQLデータベースへの接続情報
# 「mysql+mysqlconnector://[ユーザー名]:[パスワード]@[ホスト名]:[ポート番号]/[データベース名]」
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user:password@host/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/MW81'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 追跡機能を無効化

# SQLAlchemyインスタンスを作成し、Flaskアプリに紐付ける
db = SQLAlchemy(app)

# --- ここにテーブル定義などを記述 ---
class T_instructors2(db.Model):
    f_instructor_id = db.Column(db.Integer, primary_key=True)
    f_instructor_name = db.Column(db.String(25), nullable=False)
    f_instructor_tel = db.Column(db.String(11), nullable=True)

class T_students(db.Model):
    f_student_id = db.Column(db.Integer, primary_key=True)
    f_student_name = db.Column(db.String(25), nullable=False)
    f_student_tel = db.Column(db.String(11), nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# アプリケーションコンテキストをプッシュしてテーブルを作成
with app.app_context():
    db.create_all()

# --- ここからFlaskのルートを記述 ---
@app.route('/')
def index():
    # 例：データベースにユーザーを追加
    # user = User(username='testuser', email='test@example.com')
    # user = User(username='', email='w81_user@example.com')
    # db.session.add(user)
    instructor = T_instructors2(f_instructor_id=504, f_instructor_name = '長屋真琴')
    db.session.add(instructor)
    db.session.commit()
    return 'Hello, World! User created.'

if __name__ == '__main__':
    app.run(debug=True)
