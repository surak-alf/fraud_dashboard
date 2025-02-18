Create an interactive dashboard using Dash for visualizing fraud insights. The Flask backend will serve data, while Dash will handle frontend visualizations.

* **Flask Endpoint**: Add a Flask endpoint that reads fraud data from a CSV file and serves summary statistics and fraud trends through API endpoints.  This endpoint will be separate from the model prediction endpoint.
* **Dash Frontend**: Use Dash to handle the frontend visualizations.
* **Dashboard Insights**:
    * Display total transactions, fraud cases, and fraud percentages in summary boxes.
    * Display a line chart showing the number of detected fraud cases over time.
    * Analyze where fraud is occurring geographically (e.g., using a map or choropleth chart).
    * Show a bar chart comparing the number of fraud cases across different devices.
    * Show a chart comparing the number of fraud cases across different browsers.
 
<pre>
fraud_dashboard/
├── data/
│   └── fraud_data.csv
├── api/
│   ├── app.py
│   └── requirements.txt
├── dashboard/
│   ├── dash_app.py
│   └── requirements.txt
└── run.py
</pre>
