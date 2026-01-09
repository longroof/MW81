from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

app = Flask(__name__)

# データベース接続設定
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'MW81',
    'charset': 'utf8mb4'
}

@contextmanager
def get_db_connection():
    """データベース接続のコンテキストマネージャー"""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        yield connection
    except Error as e:
        print(f"データベース接続エラー: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()

@app.route('/query', methods=['POST'])
def execute_query():
    """SELECT文を実行して結果を返す"""
    try:
        data = request.get_json()
        sql = data.get('sql', '')
        
        if not sql:
            return jsonify({'error': 'SQL文が指定されていません'}), 400
        
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            
            return jsonify({
                'success': True,
                'row_count': len(results),
                'data': results
            })
    
    except Error as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/execute', methods=['POST'])
def execute_statement():
    """INSERT/UPDATE/DELETE文を実行"""
    try:
        data = request.get_json()
        sql = data.get('sql', '')
        
        if not sql:
            return jsonify({'error': 'SQL文が指定されていません'}), 400
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            return jsonify({
                'success': True,
                'affected_rows': affected_rows,
                'message': f'{affected_rows}行が影響を受けました'
            })
    
    except Error as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/users', methods=['GET'])
def get_users():
    """サンプル: ユーザー一覧を取得"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            cursor.close()
            
            return jsonify({
                'success': True,
                'data': users
            })
    
    except Error as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """サンプル: 特定のユーザーを取得（パラメータ化クエリ）"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            # SQLインジェクション対策: パラメータ化クエリを使用
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            
            if user:
                return jsonify({
                    'success': True,
                    'data': user
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'ユーザーが見つかりません'
                }), 404
    
    except Error as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """データベース接続確認"""
    try:
        with get_db_connection() as conn:
            if conn.is_connected():
                db_info = conn.get_server_info()
                return jsonify({
                    'status': 'healthy',
                    'database': 'connected',
                    'server_version': db_info
                })
    except Error as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)