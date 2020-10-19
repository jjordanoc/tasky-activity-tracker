-- SQLite
CREATE TABLE IF NOT EXISTS buttons (
    user_id INTEGER,
    name TEXT NOT NULL,
    timespan TEXT NOT NULL,
    multiplier TEXT NOT NULL,
    color TEXT NOT NULL,
    reset_date TEXT NOT NULL,
    count INTEGER DEFAULT 0,
    button_id INTEGER PRIMARY KEY AUTOINCREMENT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
    