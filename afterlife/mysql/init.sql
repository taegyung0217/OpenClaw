SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS afterlife;
USE afterlife;

CREATE TABLE IF NOT EXISTS souls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password_hash VARCHAR(255),
    role ENUM('soul', 'admin') DEFAULT 'soul',
    -- 점수 대신 선/악/무 상태 관리 (기본값: 무)
    alignment ENUM('선', '악', '무') DEFAULT '무',
    session_token VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    password_hash VARCHAR(255),
    position ENUM('junior', 'senior', 'chief') DEFAULT 'junior',
    annual_leave INT DEFAULT 15,
    session_token VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 나머지 테이블(queue_tickets, posts, comments)은 기존과 동일하므로 생략하거나 유지하세요.

INSERT INTO souls (name, email, password_hash, role, alignment) VALUES
('홍길동', 'hong@afterlife.com', 'password123', 'soul', '선'),
('나쁜놈', 'bad@afterlife.com', 'password123', 'soul', '악');

INSERT INTO employees (name, password_hash, position) VALUES
('employee', 'employee123', 'junior'),
('admin', 'admin1234', 'chief');
