-- Sample data for development

-- Insert sample stores
INSERT INTO stores (name, address, phone) VALUES
('테이블오더 강남점', '서울시 강남구 테헤란로 123', '02-1234-5678'),
('테이블오더 홍대점', '서울시 마포구 홍익로 456', '02-2345-6789');

-- Insert sample tables (PIN: 1234 hashed with SHA-256)
INSERT INTO tables (store_id, table_number, pin, session_status) VALUES
(1, 1, '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'INACTIVE'),
(1, 2, '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'INACTIVE'),
(1, 3, '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'INACTIVE'),
(2, 1, '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'INACTIVE'),
(2, 2, '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'INACTIVE');

-- Insert sample menus
INSERT INTO menus (store_id, name, price, description, category, display_order) VALUES
(1, '김치찌개', 8000, '얼큰한 김치찌개', '찌개류', 1),
(1, '된장찌개', 7000, '구수한 된장찌개', '찌개류', 2),
(1, '제육볶음', 9000, '매콤한 제육볶음', '볶음류', 3),
(1, '불고기', 12000, '달콤한 불고기', '구이류', 4),
(1, '공기밥', 1000, '흰쌀밥', '밥류', 5),
(2, '파스타', 13000, '크림 파스타', '양식', 1),
(2, '피자', 18000, '치즈 피자', '양식', 2),
(2, '샐러드', 8000, '신선한 샐러드', '샐러드', 3);

-- Insert sample admin users (password: admin123 hashed with bcrypt)
INSERT INTO users (store_id, username, password, role) VALUES
(1, 'admin1', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'ADMIN'),
(2, 'admin2', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'ADMIN');
