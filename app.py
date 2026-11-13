from flask import Flask, redirect, render_template, request, session, jsonify, url_for
import sqlite3
import random

from helper import headlines

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.run(debug=True)

con = sqlite3.connect("decisions.db", check_same_thread=False)
con.row_factory = sqlite3.Row
db = con.cursor()

@app.route("/")
def home():
    print("CURRENT HOME ROUTE RUNNING")
    ran_headline = random.randint(0,len(headlines)-1)
    headline = headlines[ran_headline]
    trees = db.execute("SELECT title, slug FROM trees").fetchall()
    count = db.execute("SELECT COUNT(title) FROM trees").fetchone()["COUNT(title)"]
    ran_tree = random.randint(0, count-1)
    question = trees[ran_tree]["title"]
    slug = trees[ran_tree]["slug"]
    return render_template("home.html", headline = headline, question = question, slug = slug)

@app.route("/category/<category>")
def category(category):
    if category == "all":
        trees = db.execute("""
        SELECT trees.title, trees.slug,
        GROUP_CONCAT(categories.category) AS categories
        FROM trees
        JOIN tree_categories ON trees.id = tree_categories.tree_id
        JOIN categories ON categories.id = tree_categories.category_id
        GROUP BY trees.id
        """).fetchall()
    else:
        trees = db.execute("""
        SELECT trees.title, trees.slug,
        GROUP_CONCAT(categories.category) AS categories
        FROM trees
        JOIN tree_categories ON trees.id = tree_categories.tree_id
        JOIN categories ON categories.id = tree_categories.category_id
        WHERE trees.id IN (
        SELECT tree_id 
        FROM tree_categories
        JOIN categories ON categories.id = tree_categories.category_id
        WHERE categories.category = ?
        )
        GROUP BY trees.id
        """, (category,)).fetchall()
    category = category.capitalize()
    return render_template("category.html", trees = trees, category = category) 

@app.route("/tree/<slug>") #methods: get and post 
def tree(slug):
    tree = db.execute("""
    SELECT * 
    FROM trees 
    WHERE slug = ?
    """, (slug,)).fetchall()
    return render_template("tree.html", slug = slug, tree=tree)

@app.route("/api/tree/<slug>")
def data(slug):
    tree = db.execute("""
    SELECT * 
    FROM trees 
    WHERE slug = ?
    """, (slug,)).fetchone()

    tree_id = db.execute("SELECT id FROM trees WHERE slug = ?", (slug,)).fetchone()["id"]
    nodes = {}
    for node in db.execute("SELECT * FROM nodes WHERE tree_id = ?", (tree_id,)):
        nodes[node["id"]] = {"text": node["text"], "is_result": bool(node["is_result"]), "options": []}

    for option in db.execute("SELECT * FROM options WHERE node_id IN (SELECT id FROM nodes WHERE tree_id = ?)", (tree_id,)):
        nodes[option["node_id"]]["options"].append(
            {"label": option["label"], "next": option["next_node_id"]}
        )

    return jsonify({"title": tree["title"], "start": tree["start_node_id"], "nodes": nodes})

@app.route("/tree/")
def surprise():
    tree = db.execute("SELECT slug FROM trees ORDER BY RANDOM() LIMIT 1").fetchone()
    return redirect(url_for("tree", slug=tree["slug"]))