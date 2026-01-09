CREATE DATABASE shop_db;
USE shop_db;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    description TEXT,
    image_url VARCHAR(255)
);

-- サンプルデータの挿入
INSERT INTO products (name, price, description, image_url) VALUES
('スマートウォッチ', 15000, '最新機能搭載の腕時計型デバイス。', 'https://via.placeholder.com/150'),
('ワイヤレスイヤホン', 8000, '高音質でノイズキャンセリング付き。', 'https://via.placeholder.com/150'),
('ノートPC', 120000, '軽量で持ち運びに便利なハイスペックPC。', 'https://via.placeholder.com/150');