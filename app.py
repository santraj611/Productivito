# Main flask app
from flask import Flask, render_template, jsonify
import sqlite3
from graphs import generate_graph
from datetime import datetime, timedelta

app = Flask(__name__)

# Helper function to fetch data
def fetch_data(query, params=()):
    conn = sqlite3.connect("pc_usage.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weekly-summary")
def weekly_summary():
    one_week_ago = datetime.now() - timedelta(days=7)
    data = fetch_data("SELECT date, SUM(duration_seconds) FROM usage_data WHERE date >= ? GROUP BY date", (one_week_ago.date(),))
    return render_template("weekly_summary.html", data=data)

@app.route("/monthly-summary")
def monthly_summary():
    one_month_ago = datetime.now() - timedelta(days=30)
    data = fetch_data("SELECT date, SUM(duration_seconds) FROM usage_data WHERE date >= ? GROUP BY date", (one_month_ago.date(),))
    return render_template("monthly_summary.html", data=data)

@app.route("/graph")
def graph():
    graph_url = generate_graph() # Note: graph_url is just the path for the grap
    if not graph_url:
        return "No data available to generate a graph."
    return render_template("graph.html", graph_url=graph_url)

if __name__ == "__main__":
    app.run(debug=True)
