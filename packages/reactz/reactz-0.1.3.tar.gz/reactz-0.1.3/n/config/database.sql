-- Структура таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    fullname VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Структура таблицы услуг
CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Структура таблицы заявок
CREATE TABLE IF NOT EXISTS requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(20) NOT NULL,
    service_date DATETIME NOT NULL,
    service_id INT,
    custom_service TEXT,
    payment_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'новая',
    cancel_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Добавляем стандартные услуги
INSERT INTO services (name, description) VALUES 
('Общий клининг', 'Стандартная уборка помещений'),
('Генеральная уборка', 'Полная глубокая уборка всего помещения'),
('Послестроительная уборка', 'Уборка после ремонта или строительства'),
('Химчистка ковров', 'Профессиональная чистка ковров и ковровых покрытий'),
('Химчистка мебели', 'Профессиональная чистка мягкой мебели');

-- Создаем админа по умолчанию (пароль: admin123)
INSERT INTO users (username, password, email, fullname, phone, role) 
VALUES ('admin', '$2y$10$9KZMkdwbQYqzLQfPnFjpMOcGJ5lkTEQXHV5pyAD7y0hD9jwE0.DCG', 'admin@example.com', 'Администратор', '+7(000)-000-00-00', 'admin');