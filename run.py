import subprocess
import time

# Start Flask API
flask_process = subprocess.Popen(['python', 'api/app.py'])

# Wait for Flask to start (adjust sleep time if needed)
time.sleep(2)  

# Start Dash app
dash_process = subprocess.Popen(['python', 'dashboard/dash_app.py'])

# Keep the script running to keep both processes alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
    flask_process.terminate()
    dash_process.terminate()