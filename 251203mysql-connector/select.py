# select.py
import mysql.connector
from flask import Flask, render_template
from db_config import DB_CONFIG  # 接続情報をインポート

app = Flask(__name__)

def get_data_from_db(sql_query):
    """
    指定されたSQLクエリを実行し、結果のデータとカラム名を取得します。
    """
    connection = None
    cursor = None
    data = None
    columns = None
    error = None

    try:
        # データベースに接続
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # SQLの実行
        cursor.execute(sql_query)

        # 全てのデータを取得
        data = cursor.fetchall()

        # カラム名（フィールド名）を取得
        # cursor.descriptionはタプルのタプルで、各タプルの最初の要素がカラム名です。
        if cursor.description:
            columns = [i[0] for i in cursor.description]

    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
        error = f"データベースエラーが発生しました: {err}"
        data = None  # エラー時はデータをクリア

    finally:
        # 接続を閉じる
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return data, columns, error

@app.route('/')
def select_data():
    """
    ルートURL ('/') にアクセスされたときに実行される関数。
    データベースからデータを取得し、HTMLテーブルとして表示します。
    """
    # 実行したいSELECT文
    # 📝 例: 'users' テーブルの 'id', 'name', 'email' を取得
    # SQL = "SELECT id, name, email FROM users ORDER BY id DESC LIMIT 10"
    SQL = "select * from t_instructors limit 10"

    # データベースからデータを取得
    data, columns, error = get_data_from_db(SQL)

    # テンプレートにデータを渡してレンダリング
    return render_template(
        'results.html',
        data=data,          # 取得したデータ (タプルのリスト)
        columns=columns,    # カラム名のリスト
        error=error         # エラーメッセージ
    )

if __name__ == '__main__':
    # デバッグモードでアプリケーションを実行
    app.run(debug=True)