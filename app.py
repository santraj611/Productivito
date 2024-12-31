# Main flask app
from flask import Flask, render_template, jsonify
from graphs import generate_graph, generate_monthly_summary, generate_weekly_summary

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weekly-summary")
def weekly_summary():
    graph_url = generate_weekly_summary() # Note: graph_url is just the path for the grap
    if not graph_url:
        return "No data available to generate a graph."
    return render_template("weekly_summary.html", graph_url=graph_url)

@app.route("/monthly-summary")
def monthly_summary():
    graph_url = generate_monthly_summary() # Note: graph_url is just the path for the grap
    if not graph_url:
        return "No data available to generate a graph."
    return render_template("monthly_summary.html", graph_url=graph_url)

@app.route("/graph")
def graph():
    graph_url = generate_graph() # Note: graph_url is just the path for the grap
    if not graph_url:
        return "No data available to generate a graph."
    return render_template("graph.html", graph_url=graph_url)

if __name__ == "__main__":
    app.run(debug=True)
