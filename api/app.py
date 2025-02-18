import os
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Construct path to data directory using os.path
data_dir = os.path.join(os.path.dirname(__file__), '../data')
csv_file_path = os.path.join(data_dir, 'fraud_data.csv')

# Load your data
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"Error: '{csv_file_path}' not found. Please place it in the 'data/' directory.")
    exit()

# API endpoints

@app.route('/api/summary')
def summary():
    total_transactions = len(df)
    fraud_cases = df['class'].sum()
    fraud_percentage = (fraud_cases / total_transactions) * 100 if total_transactions > 0 else 0

    return jsonify({
        'total_transactions': int(total_transactions),
        'fraud_cases': int(fraud_cases),
        'fraud_percentage': float(fraud_percentage)
    })

@app.route('/api/fraud_over_time')
def fraud_over_time():
    # Assuming 'time_since_signup' can represent time for now
    df['time_since_signup'] = pd.to_datetime(df['time_since_signup'], unit='s')
    fraud_over_time_data = df[df['class'] == 1].groupby(pd.Grouper(key='time_since_signup', freq='D')).size().reset_index(name='count')
    fraud_over_time_data['time_since_signup'] = fraud_over_time_data['time_since_signup'].dt.strftime('%Y-%m-%d') # Format date
    return jsonify(fraud_over_time_data.to_dict(orient='records'))

@app.route('/api/fraud_by_location')
def fraud_by_location():
    fraud_by_location_data = df[df['class'] == 1]['country_grouped_United States'].value_counts().to_dict()
    return jsonify(fraud_by_location_data)

@app.route('/api/fraud_by_device_browser')
def fraud_by_device_browser():
    # Group by browser and sum fraud cases.  Adapt as needed for device info.
    fraud_by_device_browser_data = df[df['class'] == 1].groupby('browser_Chrome').size().to_dict()
    return jsonify(fraud_by_device_browser_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)