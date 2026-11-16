from flask import Flask, redirect, render_template, request, session, jsonify, url_for, flash
import sqlite3
import random
import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from helper import headlines

load_dotenv()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = os.environ.get("SECRET_KEY")
if __name__ == "__main__":
    app.run(debug=True)

con = sqlite3.connect("decisions.db", check_same_thread=False)
con.row_factory = sqlite3.Row
db = con.cursor()

headline_random = random.Random()

@app.route("/")
def home():
    ran_headline = headline_random.randint(0, len(headlines) - 1)
    headline = headlines[ran_headline]
    trees = db.execute("SELECT title, slug FROM trees").fetchall()
    random.seed(date.today().toordinal())
    today_tree = random.choice(trees)
    question = today_tree["title"]
    slug = today_tree["slug"]
    return render_template("home.html", headline = headline, question = question, slug = slug)

@app.route("/category/<category>")
def category(category):
    if category == "all":
        trees = db.execute("""
        SELECT trees.id, trees.title, trees.slug,
        GROUP_CONCAT(categories.category) AS categories,
        saved_trees.tree_id IS NOT NULL AS saved
        FROM trees
        JOIN tree_categories ON trees.id = tree_categories.tree_id
        JOIN categories ON categories.id = tree_categories.category_id
        LEFT JOIN saved_trees
        ON trees.id = saved_trees.tree_id
        AND saved_trees.user_id = ?
        GROUP BY trees.id
        """, (session.get("user_id"),)).fetchall()
    else:
        trees = db.execute("""
        SELECT trees.id, trees.title, trees.slug,
        GROUP_CONCAT(categories.category) AS categories,
        saved_trees.tree_id IS NOT NULL AS saved
        FROM trees
        JOIN tree_categories ON trees.id = tree_categories.tree_id
        JOIN categories ON categories.id = tree_categories.category_id
        LEFT JOIN saved_trees
        ON trees.id = saved_trees.tree_id
        AND saved_trees.user_id = ?
        WHERE trees.id IN (
        SELECT tree_id 
        FROM tree_categories
        JOIN categories ON categories.id = tree_categories.category_id
        WHERE categories.category = ?
        )
        GROUP BY trees.id
        """, (session.get("user_id"), category)).fetchall()
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

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user is None:
            flash("Invalid username/password")
            return redirect("/login")       
        if not check_password_hash(user["hash"], password):
            flash("Invalid username/password")
            return redirect("/login")
        session["user_id"] = user["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            flash("Passwords do not match")
            return redirect("/register")
        password_hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, password_hash))
            con.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists")
            return redirect("/register")
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/delete")
def delete():
    db.execute("DELETE FROM users WHERE id = ?", (session["user_id"],))
    con.commit()
    session.clear()
    return redirect("/")

@app.route("/save/<tree_id>", methods=["POST"])
def save(tree_id):
    if "user_id" not in session:
        return {"success": False, "error": "login required"}, 401 #or use @login required
    row = db.execute("SELECT * FROM saved_trees WHERE user_id = ? AND tree_id = ?", (session["user_id"], tree_id)).fetchone()
    if row:
        db.execute("DELETE FROM saved_trees WHERE user_id = ? AND tree_id = ?", (session["user_id"], tree_id))
        saved = False
    else:
        db.execute("INSERT INTO saved_trees (user_id, tree_Id) VALUES (?, ?)", (session["user_id"], tree_id))
        saved = True
    con.commit()
    return {"success": True, "saved": saved}

@app.route("/saved")
def saved():
    if "user_id" not in session:
        return redirect("/login")
    trees = db.execute("""
    SELECT trees.id, trees.title, trees.slug,
    GROUP_CONCAT(categories.category) AS categories,
    1 AS saved
    FROM trees
    JOIN tree_categories ON trees.id = tree_categories.tree_id
    JOIN categories ON categories.id = tree_categories.category_id
    WHERE trees.id IN (
    SELECT tree_id FROM saved_trees WHERE user_id = ?)
    GROUP BY trees.id
    """, (session.get("user_id"),)).fetchall()
    return render_template("save.html", trees = trees)
