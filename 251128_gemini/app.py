from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, MetaData, Table, select

app = Flask(__name__)

# ==========================================
# MySQL データベース接続設定
# ==========================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/MW81?charset=utf8mb4'
app.config['SQLALCHEMY_ECHO'] = False # 必要に応じてTrueにすると、裏で生成されたSQLを確認できます
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    columns = []
    data = []
    error = None
    table_name = ""

    if request.method == 'POST':
        table_name = request.form.get('table_name')
        
        try:
            # 1. テーブルの存在確認 (Inspector)
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()

            if table_name in existing_tables:
                # 2. メタデータの作成 (一時的なコンテナ)
                metadata = MetaData()
                
                # 3. テーブル定義の読み込み (Reflection)
                # SQLを書く代わりに、DBから構造を読み込んでPythonオブジェクトにします
                target_table = Table(table_name, metadata, autoload_with=db.engine)

                # 4. クエリの構築と実行 (Query Builder)
                # "SELECT * FROM table_name" に相当する処理をオブジェクトで行います
                stmt = select(target_table)
                
                with db.engine.connect() as conn:
                    result = conn.execute(stmt)
                    
                    columns = result.keys()
                    data = result.fetchall()
            else:
                if existing_tables:
                    error = f"テーブル '{table_name}' は存在しません。利用可能: {', '.join(existing_tables)}"
                else:
                    error = "このデータベースにはテーブルが存在しません。"

        except Exception as e:
            error = f"エラーが発生しました: {str(e)}"

    return render_template('index.html', columns=columns, data=data, error=error, table_name=table_name)

if __name__ == '__main__':
    app.run(debug=True)