-- データベースの作成
CREATE DATABASE IF NOT EXISTS shopping_site CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shopping_site;

-- 商品テーブル
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 注文テーブル
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 注文詳細テーブル
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- サンプルデータの挿入
INSERT INTO products (name, description, price, stock, image_url) VALUES
('ノートパソコン', '高性能なビジネス向けノートパソコン', 89800.00, 15, 'https://via.placeholder.com/300x200?text=Laptop'),
('ワイヤレスマウス', 'Bluetooth対応の静音マウス', 2980.00, 50, 'https://via.placeholder.com/300x200?text=Mouse'),
('キーボード', 'メカニカルキーボード RGB対応', 12800.00, 30, 'https://via.placeholder.com/300x200?text=Keyboard'),
('モニター', '27インチ 4K解像度モニター', 45000.00, 20, 'https://via.placeholder.com/300x200?text=Monitor'),
('Webカメラ', 'Full HD 1080p Webカメラ', 6800.00, 40, 'https://via.placeholder.com/300x200?text=Webcam'),
('ヘッドセット', 'ノイズキャンセリング機能付き', 8900.00, 35, 'https://via.placeholder.com/300x200?text=Headset'),
('USBハブ', '7ポート USB3.0対応', 3200.00, 60, 'https://via.placeholder.com/300x200?text=USB+Hub'),
('外付けSSD', '1TB ポータブルSSD', 15800.00, 25, 'https://via.placeholder.com/300x200?text=SSD');