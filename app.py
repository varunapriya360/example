import matplotlib
matplotlib.use("Agg")

from flask import Flask, render_template, request, redirect
import sqlite3
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

#DB = "expenses.db"
DB = os.getenv("DB_NAME", "expenses.db")
APP_PORT = int(os.getenv("APP_PORT", 5000))

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            category TEXT,
            amount REAL,
            type TEXT
        )
        """)

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        category = request.form["category"]
        amount = float(request.form["amount"])
        type_ = request.form["type"]

        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO expenses (category, amount, type) VALUES (?, ?, ?)",
                (category, amount, type_)
            )

        return redirect("/")

    with sqlite3.connect(DB) as conn:
        data = conn.execute("SELECT * FROM expenses").fetchall()

    return render_template("index.html", expenses=data)

@app.route("/chart")
def chart():
    os.makedirs("static", exist_ok=True)

    with sqlite3.connect(DB) as conn:
        data = conn.execute(
            "SELECT category, SUM(amount) FROM expenses WHERE type='expense' GROUP BY category"
        ).fetchall()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title("Expense Breakdown")
    plt.savefig("static/chart.png")
    plt.clf()

    return render_template("report.html")
