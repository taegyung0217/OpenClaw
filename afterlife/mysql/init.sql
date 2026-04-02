CREATE DATABASE IF NOT EXISTS afterlife;
USE afterlife;

CREATE TABLE IF NOT EXISTS souls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password_hash VARCHAR(255),
    role ENUM('soul', 'admin') DEFAULT 'soul',
    karma_score INT DEFAULT 0,
    session_token VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    password_hash VARCHAR(255),
    position ENUM('junior', 'senior', 'chief') DEFAULT 'junior',
    annual_leave INT DEFAULT 15,
    session_token VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS queue_tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    soul_id INT,
    ticket_number INT,
    status ENUM('waiting', 'processing', 'done') DEFAULT 'waiting',
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    soul_id INT,
    title VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT,
    soul_id INT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO souls (name, email, password_hash, role, karma_score) VALUES
('홍길동', 'hong@afterlife.com', 'password123', 'soul', 30),
('나쁜놈', 'bad@afterlife.com', 'password123', 'soul', -999);

INSERT INTO employees (name, password_hash, position) VALUES
('저승사자A', 'employee123', 'junior'),
('염라대왕', 'admin1234', 'chief');
