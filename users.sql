-- Add users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

-- Add saved-trees table
CREATE TABLE saved_trees (
    user_id INTEGER NOT NULL,
    tree_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, tree_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (tree_id) REFERENCES trees(id)
);

-- Add history table