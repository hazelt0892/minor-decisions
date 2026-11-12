import glob
import json
import sqlite3

con = sqlite3.connect("decisions.db")
db = con.cursor()

db.executescript("DELETE FROM trees; DELETE FROM nodes; DELETE FROM options; DELETE FROM categories; DELETE FROM tree_categories;")

def slugify(title):
    slug = title.lower()
    for c in slug:
        if not c.isalnum() and c != "-":
            slug = slug.replace(c, "-")
            slug = slug.strip("-")
    return slug

for path in glob.glob("trees/*.json"):
    with open(path) as f:
        tree = json.load(f)

    slug = slugify(tree["title"])

    db.execute("INSERT INTO trees (title, slug) VALUES (?, ?)", (tree["title"], slug)) # maybe add description (and in json)
    tree_id = db.lastrowid

    ids = {}
    for name, node in tree["nodes"].items():
        db.execute("INSERT INTO nodes (tree_id, text, is_result) VALUES (?, ?, ?)", (tree_id, node["text"], 1 if node.get("result") else 0))
        ids[name] = db.lastrowid
    
    for category in tree["categories"]:
        db.execute("INSERT OR IGNORE INTO categories (category) VALUES (?)", (category,))
        db.execute("SELECT id FROM categories WHERE category = ?", (category,))
        category_id = db.fetchone()[0]
        db.execute("INSERT OR IGNORE INTO tree_categories (tree_id, category_id) VALUES (?, ?)", (tree_id, category_id))
        
    for name, node in tree["nodes"].items():
        if "yes" in node and "no" in node:
            options = [
                {"label": "yes", "next": node["yes"]},
                {"label": "no", "next": node["no"]}
            ]
        elif "options" in node:
            options = node["options"]
        else:
            options = []

        for option in options:
            db.execute("INSERT INTO options (node_id, label, next_node_id) VALUES (?, ?, ?)", (ids[name], option["label"], ids[option["next"]]))

    db.execute("UPDATE trees SET start_node_id = ? WHERE id = ?", (ids[tree["start"]], tree_id))

con.commit()
con.close()