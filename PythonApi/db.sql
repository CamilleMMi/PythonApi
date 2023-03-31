DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS watching_list;

-- Creation of the users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Creation of the watching list table
CREATE TABLE watching_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    viewing_name VARCHAR(255) NOT NULL,
    platform VARCHAR(255) NOT NULL,
    advancement VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users(email, username, password) VALUES
    ("admin.email@gmail.com","admin", "password"),
    ("camillemichaudmeli@gmail.com","Camille", "Camille"),
    ("userlambda@gmail.com","User", "password");

INSERT INTO watching_list(viewing_name, platform, advancement, user_id) VALUES
    ("naruto", "netflix", "episode 12 saison 2", 1),
    ("one piece", "netflix", "episode 1 saison 1", 1),
    ("split", "streaming", "", 1),
    ("Squeezie thread horreur", "youtube", "12:10", 1),
    ("Batman", "netflix", "", 2),
    ("Heredity", "amazon prime video", "1H 10", 2);