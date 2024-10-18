-- Drop tables if they already exist
DROP TABLE IF EXISTS customizations;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS burgers;
DROP TABLE IF EXISTS users;

-- Create table for burgers
CREATE TABLE IF NOT EXISTS burgers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2)
);

-- Create table for orders
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    burger_id INT,
    quantity INT,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(255),
    FOREIGN KEY (burger_id) REFERENCES burgers(id)
);

-- Create table for customizations
CREATE TABLE IF NOT EXISTS customizations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    customization TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Create table for users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Insert some initial burgers
INSERT IGNORE INTO burgers (name, description, price) VALUES ("OSTBURGARE", "", 120);
INSERT IGNORE INTO burgers (name, description, price) VALUES ("VEGGIEBURGARE", "", 100);
INSERT IGNORE INTO burgers (name, description, price) VALUES ("BACONBURGARE", "", 130);