from flask import Flask, render_template_string, request, jsonify
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

app = Flask(__name__)

# データベース接続設定（ここで認証情報を設定）
DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'MW81'
}

# データベース接続URL
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# SQLAlchemyエンジンの作成
engine = create_engine(DATABASE_URL)

# HTMLテンプレート
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Viewer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .form-group {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        select, input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        button:hover {
            background-color: #45a049;
        }
        .table-container {
            margin-top: 30px;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .error {
            color: #d32f2f;
            background-color: #ffebee;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .info {
            color: #1976d2;
            background-color: #e3f2fd;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .record-count {
            margin: 15px 0;
            font-weight: bold;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Database Table Viewer</h1>
        
        <form method="POST" action="/">
            <div class="form-group">
                <label for="table_name">テーブル名を選択:</label>
                <select name="table_name" id="table_name">
                    <option value="">-- テーブルを選択してください --</option>
                    {% for table in tables %}
                    <option value="{{ table }}" {% if table == selected_table %}selected{% endif %}>
                        {{ table }}
                    </option>
                    {% endfor %}
                </select>
            </div>
            <button type="submit">データを表示</button>
        </form>

        {% if error %}
        <div class="error">
            <strong>エラー:</strong> {{ error }}
        </div>
        {% endif %}

        {% if records %}
        <div class="record-count">
            レコード数: {{ records|length }}
        </div>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        {% for column in columns %}
                        <th>{{ column }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for record in records %}
                    <tr>
                        {% for value in record %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% elif selected_table %}
        <div class="info">
            テーブル "{{ selected_table }}" にはデータがありません。
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def get_table_names():
    """データベース内の全テーブル名を取得"""
    try:
        inspector = inspect(engine)
        return inspector.get_table_names()
    except SQLAlchemyError as e:
        print(f"テーブル名取得エラー: {e}")
        return []

def get_table_data(table_name):
    """指定されたテーブルの全データを取得"""
    try:
        with engine.connect() as connection:
            # SQLインジェクション対策のため、テーブル名を検証
            inspector = inspect(engine)
            if table_name not in inspector.get_table_names():
                return None, None, "指定されたテーブルは存在しません"
            
            # データを取得
            query = text(f"SELECT * FROM {table_name}")
            result = connection.execute(query)
            
            # カラム名を取得
            columns = result.keys()
            
            # 全レコードを取得
            records = result.fetchall()
            
            return columns, records, None
    except SQLAlchemyError as e:
        return None, None, f"データ取得エラー: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    tables = get_table_names()
    selected_table = None
    columns = None
    records = None
    error = None
    
    if request.method == 'POST':
        selected_table = request.form.get('table_name')
        if selected_table:
            columns, records, error = get_table_data(selected_table)
    
    return render_template_string(
        HTML_TEMPLATE,
        tables=tables,
        selected_table=selected_table,
        columns=columns,
        records=records,
        error=error
    )

if __name__ == '__main__':
    # データベース接続テスト
    try:
        with engine.connect() as connection:
            print("データベース接続成功！")
            tables = get_table_names()
            print(f"利用可能なテーブル: {tables}")
    except SQLAlchemyError as e:
        print(f"データベース接続エラー: {e}")
    
    # Flaskアプリケーション起動
    app.run(debug=True, host='0.0.0.0', port=5000)