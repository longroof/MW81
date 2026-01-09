-- データベースの作成
CREATE DATABASE IF NOT EXISTS mw81_sample;
USE mw81_sample;

-- ユーザーテーブル
CREATE TABLE t_users (
    f_user_id INT AUTO_INCREMENT PRIMARY KEY,
    f_user_name VARCHAR(50) UNIQUE NOT NULL,
    f_user_email VARCHAR(255) UNIQUE NOT NULL,
    f_user_password_hash VARCHAR(512) NOT NULL,
    f_user_full_name VARCHAR(100),
    f_user_address TEXT,
    f_user_phone VARCHAR(20),
    f_user_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    f_user_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 商品テーブル
CREATE TABLE t_products (
    f_product_id INT AUTO_INCREMENT PRIMARY KEY,
    f_product_name VARCHAR(255) NOT NULL,
    f_product_description TEXT,
    f_product_price DECIMAL(10, 2) NOT NULL,
    f_product_stock INT NOT NULL DEFAULT 0,
    f_product_image_url VARCHAR(500),
    f_product_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    f_product_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 注文テーブル（user_idを追加）
CREATE TABLE t_orders (
    f_order_id INT AUTO_INCREMENT PRIMARY KEY,
    f_order_user_id INT,
    f_order_customer_name VARCHAR(255) NOT NULL,
    f_order_email VARCHAR(255) NOT NULL,
    f_order_address TEXT NOT NULL,
    f_order_total_amount DECIMAL(10, 2) NOT NULL,
    f_order_status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    f_order_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    f_order_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (f_order_user_id) REFERENCES t_users(f_user_id) ON DELETE SET NULL
);

-- 注文詳細テーブル
CREATE TABLE t_order_items (
    f_order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    f_order_id INT NOT NULL,
    f_product_id INT NOT NULL,
    f_order_item_quantity INT NOT NULL,
    f_order_item_price DECIMAL(10, 2) NOT NULL,
    f_order_item_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (f_order_id) REFERENCES t_orders(f_order_id) ON DELETE CASCADE,
    FOREIGN KEY (f_product_id) REFERENCES t_products(f_product_id) ON DELETE RESTRICT
);

-- サンプルユーザーの挿入（パスワード: password123）
INSERT INTO t_users (f_user_name, f_user_email, f_user_password_hash, f_user_full_name, f_user_address, f_user_phone) VALUES
('testuser', 'test@example.com', 'scrypt:32768:8:1$xOZj8QXkJHGH9LQm$c8e1f5d8f5a8c9e0b6d4a7c2f3e8d1b9a5c7e2f4d6b8a3c5e7f9d1b4a6c8e0f2d5b7a9c1e3f5d7b9a2c4e6f8d0b3a5c7e9f1d4b6a8c0e2f5d7b9a1c3e6f8d0b2a4c7e9f1d3b5a8c0e2f4d6b9a1c3e5f7d9b2a4c6e8f0d3b5a7c9e1f4d6b8a0c2e5f7d9b1a3c6e8f0d2b4a7c9e1f3d5b8a0c2e4f6d9b1a3c5e7f0d2b4a6c8e1f3d5b7a9c0e2f4d6b8a1c3e5f7d9b0a2c4e6f8d1b3a5c7e9f0d2b4a6c8e1f3d5b7a9c0e2f4d6b8a1c3e5f7d9b0a2c4e6f8', '田中 太郎', '東京都渋谷区1-1-1', '090-1234-5678'),
('adminuser', 'admin@example.com', 'scrypt:32768:8:1$xOZj8QXkJHGH9LQm$c8e1f5d8f5a8c9e0b6d4a7c2f3e8d1b9a5c7e2f4d6b8a3c5e7f9d1b4a6c8e0f2d5b7a9c1e3f5d7b9a2c4e6f8d0b3a5c7e9f1d4b6a8c0e2f5d7b9a1c3e6f8d0b2a4c7e9f1d3b5a8c0e2f4d6b9a1c3e5f7d9b2a4c6e8f0d3b5a7c9e1f4d6b8a0c2e5f7d9b1a3c6e8f0d2b4a7c9e1f3d5b8a0c2e4f6d9b1a3c5e7f0d2b4a6c8e1f3d5b7a9c0e2f4d6b8a1c3e5f7d9b0a2c4e6f8d1b3a5c7e9f0d2b4a6c8e1f3d5b7a9c0e2f4d6b8a1c3e5f7d9b0a2c4e6f8', '管理者', '東京都千代田区2-2-2', '090-8765-4321');

-- サンプルデータの挿入
INSERT INTO t_products (f_product_name, f_product_description, f_product_price, f_product_stock, f_product_image_url) VALUES
('ノートパソコン', '高性能なビジネス向けノートパソコン', 89800.00, 15, 'https://placehold.jp/300x200.png?text=Laptop'),
('ワイヤレスマウス', 'Bluetooth対応の静音マウス', 2980.00, 50, 'https://placehold.jp/300x200.png?text=Mouse'),
('キーボード', 'メカニカルキーボード RGB対応', 12800.00, 30, 'https://placehold.jp/300x200.png?text=Keyboard'),
('モニター', '27インチ 4K解像度モニター', 45000.00, 20, 'https://placehold.jp/300x200.png?text=Monitor'),
('Webカメラ', 'Full HD 1080p Webカメラ', 6800.00, 40, 'https://placehold.jp/300x200.png?text=Webcam'),
('ヘッドセット', 'ノイズキャンセリング機能付き', 8900.00, 35, 'https://placehold.jp/300x200.png?text=Headset'),
('USBハブ', '7ポート USB3.0対応', 3200.00, 60, 'https://placehold.jp/300x200.png?text=USB+Hub'),
('外付けSSD', '1TB ポータブルSSD', 15800.00, 25, 'https://placehold.jp/300x200.png?text=SSD');