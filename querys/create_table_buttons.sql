-- SQLite
CREATE TABLE IF NOT EXISTS buttons (
    user_id INTEGER,
    button_name TEXT NOT NULL,
    timespan TEXT NOT NULL,
    multiplier TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
    