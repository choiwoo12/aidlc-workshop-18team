-- Table Order System Database Schema

-- Store Table
CREATE TABLE IF NOT EXISTS stores (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    phone VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table Table
CREATE TABLE IF NOT EXISTS tables (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    store_id BIGINT NOT NULL,
    table_number INT NOT NULL,
    pin VARCHAR(64) NOT NULL,
    session_id VARCHAR(36),
    session_status VARCHAR(20) NOT NULL DEFAULT 'INACTIVE',
    session_start_time TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(id),
    UNIQUE KEY uk_store_table (store_id, table_number),
    CHECK (table_number BETWEEN 1 AND 10)
);

-- Menu Table
CREATE TABLE IF NOT EXISTS menus (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    store_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    description VARCHAR(500),
    category VARCHAR(50) NOT NULL,
    image_path VARCHAR(255),
    display_order INT NOT NULL DEFAULT 0,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(id),
    CHECK (price >= 0)
);

-- Order Table
CREATE TABLE IF NOT EXISTS orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    store_id BIGINT NOT NULL,
    table_id BIGINT NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    order_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT '대기중',
    version INT NOT NULL DEFAULT 0,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (table_id) REFERENCES tables(id),
    CHECK (total_amount >= 0)
);

-- OrderItem Table
CREATE TABLE IF NOT EXISTS order_items (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    menu_id BIGINT NOT NULL,
    menu_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    unit_price INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_id) REFERENCES menus(id),
    CHECK (quantity > 0),
    CHECK (unit_price >= 0)
);

-- OrderHistory Table
CREATE TABLE IF NOT EXISTS order_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    order_number VARCHAR(50) NOT NULL,
    store_id BIGINT NOT NULL,
    table_id BIGINT NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    order_time TIMESTAMP NOT NULL,
    total_amount INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    completed_time TIMESTAMP NOT NULL,
    archived_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- OrderHistoryItem Table
CREATE TABLE IF NOT EXISTS order_history_items (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_history_id BIGINT NOT NULL,
    menu_id BIGINT NOT NULL,
    menu_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    unit_price INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_history_id) REFERENCES order_history(id)
);

-- User Table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    store_id BIGINT NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL,
    role VARCHAR(20) NOT NULL,
    login_attempts INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(id)
);

-- Indexes for performance
CREATE INDEX idx_table_store_session ON tables(store_id, session_id);
CREATE INDEX idx_menu_store_category ON menus(store_id, category, display_order);
CREATE INDEX idx_menu_deleted ON menus(deleted);
CREATE INDEX idx_order_table_session ON orders(table_id, session_id);
CREATE INDEX idx_order_store_time ON orders(store_id, order_time);
CREATE INDEX idx_order_deleted ON orders(deleted);
CREATE INDEX idx_order_history_store_time ON order_history(store_id, archived_time);
CREATE INDEX idx_user_store ON users(store_id);
