-- Создание таблицы пользователей
CREATE TABLE users (
    chat_id INT8 PRIMARY KEY,
    user_id INT8 NOT NULL UNIQUE,
    bought_id INT NOT NULL,
    referrer_id INT8,
    discount INT DEFAULT 0,
    FOREIGN KEY (referrer_id) REFERENCES users(user_id)
);

-- Создание таблицы аккаунтов
CREATE TABLE accounts (
    acc_email TEXT PRIMARY KEY,
    acc_password TEXT NOT NULL,
    available_slot INT NOT NULL DEFAULT 0,
    games_list JSONB,
    users_list JSONB
);

-- Создание таблицы игровых ключей
CREATE TABLE keys (
    game_key VARCHAR(64) NOT NULL,
    game_name TEXT NOT NULL,
    platform TEXT NOT NULL
);

-- Создание таблицы технической поддержки
CREATE TABLE tech_support (
    admin_username TEXT NOT NULL,
    admin_chat_id INT8 NOT NULL, 
    hit_count INT NOT NULL
);

-- Создание таблицы реферальных связей
CREATE TABLE referrals (
    user_id INT8 REFERENCES users(user_id),
    referred_user_id INT8 UNIQUE REFERENCES users(user_id),
    PRIMARY KEY (user_id, referred_user_id)
);
