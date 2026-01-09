
-- DB作成（必要なら）
CREATE DATABASE IF NOT EXISTS shop_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE shop_db;

-- ユーザー
CREATE TABLE IF NOT EXISTS users (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  email        VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  name         VARCHAR(100) NOT NULL,
  created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 商品
CREATE TABLE IF NOT EXISTS products (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  name         VARCHAR(200) NOT NULL,
  description  TEXT,
  price        INT NOT NULL,              -- 円を想定（整数）
  stock        INT NOT NULL DEFAULT 0,
  image_url    VARCHAR(500),
  is_active    TINYINT(1) NOT NULL DEFAULT 1,
  created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_products_active (is_active)
) ENGINE=InnoDB;

-- 注文（ヘッダ）
CREATE TABLE IF NOT EXISTS orders (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  user_id      INT NOT NULL,
  total_amount INT NOT NULL,              -- 合計（円）
  status       VARCHAR(30) NOT NULL DEFAULT 'PAID',  -- 簡易: PAID/CREATED/CANCELLED等
  created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_orders_user
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  INDEX idx_orders_user_created (user_id, created_at)
) ENGINE=InnoDB;

-- 注文明細
CREATE TABLE IF NOT EXISTS order_items (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  order_id    INT NOT NULL,
  product_id  INT NOT NULL,
  product_name VARCHAR(200) NOT NULL,     -- 注文時点の名称を保存
  unit_price  INT NOT NULL,              -- 注文時点の単価
  quantity    INT NOT NULL,
  line_total  INT NOT NULL,
  CONSTRAINT fk_items_order
    FOREIGN KEY (order_id) REFERENCES orders(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_items_product
    FOREIGN KEY (product_id) REFERENCES products(id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  INDEX idx_items_order (order_id)
) ENGINE=InnoDB;

