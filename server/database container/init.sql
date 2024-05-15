CREATE TABLE users (
    chat_id INT8 PRIMARY KEY,
    user_id INT8 NOT NULL,
    bought_id INT NOT NULL
);

CREATE TABLE accounts (
    acc_email TEXT PRIMARY KEY,
    acc_password TEXT NOT NULL,
    available_slot INT NOT NULL DEFAULT 0,
    games_list JSONB,
    users_list JSONB
);

CREATE TABLE keys (
    game_key VARCHAR(64) NOT NULL,
    game_name TEXT NOT NULL,
    platform TEXT NOT NULL
);

CREATE TABLE tech_support (
    admin_username TEXT NOT NULL,
    admin_chat_id INT8 NOT NULL, 
    hit_count INT NOT NULL
);

