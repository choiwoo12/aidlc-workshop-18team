-- Sample Data for Table Order System

-- Insert Stores
INSERT INTO stores (name, address, phone) VALUES
('테스트 매장 1', '서울시 강남구', '02-1234-5678'),
('테스트 매장 2', '서울시 서초구', '02-2345-6789');

-- Insert Tables
INSERT INTO `table` (store_id, table_number, session_id, session_active) VALUES
(1, 1, 'test-session-001', TRUE),
(1, 2, NULL, FALSE),
(1, 3, NULL, FALSE),
(2, 1, NULL, FALSE),
(2, 2, NULL, FALSE);

-- Insert Menus
INSERT INTO menu (store_id, name, price, image_url, deleted) VALUES
(1, '김치찌개', 8000, NULL, FALSE),
(1, '된장찌개', 7000, NULL, FALSE),
(1, '비빔밥', 9000, NULL, FALSE),
(1, '불고기', 15000, NULL, FALSE),
(1, '공기밥', 1000, NULL, FALSE),
(2, '짜장면', 6000, NULL, FALSE),
(2, '짬뽕', 7000, NULL, FALSE),
(2, '탕수육', 18000, NULL, FALSE);

-- Insert Admin User (password: admin, SHA-256 hashed)
INSERT INTO `user` (store_id, username, password, role) VALUES
(1, 'admin1', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'ADMIN'),
(2, 'admin2', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'ADMIN');
