import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import json
import os

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server  # Expose the Flask server for deployment

# API base URL
API_URL = 'http://localhost:5000/api' 

app.layout = html.Div([
    html.H1("Fraud Insights Dashboard"),

    # Summary Boxes
    html.Div(id='summary-boxes', className='row'),

    # Fraud Over Time Chart
    dcc.Graph(id='fraud-over-time-chart'),

    # Fraud by Location Chart
    dcc.Graph(id='fraud-by-location-chart'),

    # Fraud by Device/Browser Chart
    dcc.Graph(id='fraud-by-device-browser-chart')
])

# Callbacks to update visualizations

@app.callback(
    Output('summary-boxes', 'children'),
    [Input('interval', 'n_intervals')]  # Add a dummy interval for initial load
)
def update_summary_boxes(n):
    summary_data = requests.get(f'{API_URL}/summary').json()
    return [
        html.Div(className='four columns', children=[
            html.H3("Total Transactions"),
            html.P(summary_data['total_transactions'])
        ]),
        html.Div(className='four columns', children=[
            html.H3("Fraud Cases"),
            html.P(summary_data['fraud_cases'])
        ]),
        html.Div(className='four columns', children=[
            html.H3("Fraud Percentage"),
            html.P(f"{summary_data['fraud_percentage']:.2f}%")
        ])
    ]

@app.callback(
    Output('fraud-over-time-chart', 'figure'),
    [Input('interval', 'n_intervals')]
)
def update_fraud_over_time_chart(n):
    fraud_data = requests.get(f'{API_URL}/fraud_over_time').json()
    df = pd.DataFrame(fraud_data)
    fig = px.line(df, x='time_since_signup', y='count', title='Fraud Cases Over Time')
    return fig

@app.callback(
    Output('fraud-by-location-chart', 'figure'),
    [Input('interval', 'n_intervals')]
)
def update_fraud_by_location_chart(n):
    location_data = requests.get(f'{API_URL}/fraud_by_location').json()
    fig = px.bar(x=list(location_data.keys()), y=list(location_data.values()), title='Fraud Cases by Location')
    return fig

@app.callback(
    Output('fraud-by-device-browser-chart', 'figure'),
    [Input('interval', 'n_intervals')]
)
def update_fraud_by_device_browser_chart(n):
    device_browser_data = requests.get(f'{API_URL}/fraud_by_device_browser').json()
    fig = px.bar(x=list(device_browser_data.keys()), y=list(device_browser_data.values()), title='Fraud Cases by Device/Browser')
    return fig

# Add a hidden interval component to trigger updates
app.layout.children.append(dcc.Interval(id='interval', interval=5*60*1000, n_intervals=0))  # Update every 5 minutes

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)