"""
Copyright @emontj 2024
"""

import requests
import plotly.graph_objs as go
from flask import render_template_string

METRICS_URL = "http://localhost:5000/metrics"

def parse_metrics():
    """
    Fetch and parse the metrics data from the /metrics endpoint.
    Returns a dictionary of parsed metrics.
    """
    response = requests.get(METRICS_URL)
    response.raise_for_status()

    metrics = {}
    for line in response.text.splitlines():
        if line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) == 2:
            metric_name, metric_value = parts
            if metric_name not in metrics:
                metrics[metric_name] = []
            metrics[metric_name].append(float(metric_value))

    return metrics

def build_dashboard():
    """
    Builds the HTML dashboard with a Plotly graph using parsed /metrics data.
    """
    metrics = parse_metrics()

    metric_name = "requests_total"
    if metric_name not in metrics:
        return "Metric not found: {}".format(metric_name)

    trace = go.Scatter(
        x=list(range(len(metrics[metric_name]))),
        y=metrics[metric_name],
        mode='lines',
        name=metric_name
    )

    figure = go.Figure(data=[trace], layout=go.Layout(
        title="HTTP Requests Total",
        xaxis=dict(title="Time (arbitrary index)"),
        yaxis=dict(title="Count"),
        template="plotly_dark"
    ))

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>Flask Dashboard</h1>
        <div id="plotly-div"></div>
        <script>
            var figure = {{ figure | safe }};
            Plotly.newPlot('plotly-div', figure.data, figure.layout);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, figure=figure.to_plotly_json())
