DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS nodes;
DROP TABLE IF EXISTS trees;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS tree_categories;

CREATE TABLE trees (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    start_node_id INTEGER
);

CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    tree_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    is_result INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (tree_id) REFERENCES trees(id)
);

CREATE TABLE options (
    id INTEGER PRIMARY KEY,
    node_id INTEGER NOT NULL,
    label TEXT NOT NULL,
    next_node_id INTEGER NOT NULL,
    FOREIGN KEY (node_id) REFERENCES nodes(id),
    FOREIGN KEY (next_node_id) REFERENCES nodes(id)
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL UNIQUE
);

CREATE TABLE tree_categories (
    tree_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (tree_id, category_id),
    FOREIGN KEY (tree_id) REFERENCES trees(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Add users table
-- Add history table 