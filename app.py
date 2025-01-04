# Main flask app
from flask import Flask, render_template, jsonify
from graphs import generate_graph, generate_monthly_summary, generate_weekly_summary
from states import get_date, get_week, get_month, total_screen_time

app = Flask(__name__)

@app.route("/")
def home():
    today =  str(get_date())
    week_ago = get_week()
    month_ago = get_month()
    total_st = int(total_screen_time(today))
    this_week = int(total_screen_time(week_ago))
    this_month = int(total_screen_time(month_ago))
    return render_template("index.html", today_st=total_st, this_week=this_week, this_month=this_month)

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
