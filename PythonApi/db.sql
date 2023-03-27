DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS shopping_list;

-- Creation of the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Creation of the watching list table
CREATE TABLE watching_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    viewing_name VARCHAR(255) NOT NULL,
    platform VARCHAR(255) NOT NULL,
    advancement VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);