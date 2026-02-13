import matplotlib
matplotlib.use("Agg")

from flask import Flask, render_template, request, redirect, Response
import sqlite3
import matplotlib.pyplot as plt
import os
import time

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

DB = os.getenv("DB_NAME", "expenses.db")
APP_PORT = int(os.getenv("APP_PORT", 5000))

# --------------------
# Prometheus Metrics
# --------------------
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency",
    ["endpoint"]
)

EXPENSE_ADDED = Counter(
    "expenses_added_total",
    "Total number of expenses added"
)

# --------------------
# Database
# --------------------
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

# --------------------
# Routes
# --------------------
@app.route("/", methods=["GET", "POST"])
def index():
    start_time = time.time()
    REQUEST_COUNT.labels(request.method, "/").inc()

    if request.method == "POST":
        category = request.form["category"]
        amount = float(request.form["amount"])
        type_ = request.form["type"]

        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO expenses (category, amount, type) VALUES (?, ?, ?)",
                (category, amount, type_)
            )

        EXPENSE_ADDED.inc()

        REQUEST_LATENCY.labels("/").observe(time.time() - start_time)
        return redirect("/")

    with sqlite3.connect(DB) as conn:
        data = conn.execute("SELECT * FROM expenses").fetchall()

    REQUEST_LATENCY.labels("/").observe(time.time() - start_time)
    return render_template("index.html", expenses=data)

@app.route("/chart")
def chart():
    start_time = time.time()
    REQUEST_COUNT.labels("GET", "/chart").inc()

    os.makedirs("static", exist_ok=True)

    with sqlite3.connect(DB) as conn:
        data = conn.execute(
            "SELECT category, SUM(amount) FROM expenses WHERE type='expense' GROUP BY category"
        ).fetchall()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title("Expense Breakdown")
    plt.savefig("static/chart.png")
    plt.clf()

    REQUEST_LATENCY.labels("/chart").observe(time.time() - start_time)
    return render_template("report.html")

# --------------------
# Metrics Endpoint
# --------------------
@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

# --------------------
# App Start
# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)
