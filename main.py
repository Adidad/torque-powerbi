from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

# Replace this with your real Power BI Push URL from Step 1
POWER_BI_URL = "https://api.powerbi.com/beta/b4c6b754-54e3-41e4-a8da-304355c62816/datasets/34fe22e9-4150-4f54-8141-63905227d0c6/rows?experience=power-bi&key=zFkMSWchr%2BhtgyD2nWHXTa4DyRO0CcSWACy7eFi6YXCUsyIkNravbBbEAJ9Jlw7Yg0xXRsjgpKbh4M4HIpLT6Q%3D%3D"

@app.route('/')
def index():
    return "Torque OBD Flask Server is Running!"

@app.route('/obd', methods=['POST'])
def receive_obd_data():
    # Check if it's from Torque app
    if "Torque" not in request.headers.get("User-Agent", ""):
        return "Expected request from Torque app", 400

    data = request.form.to_dict()
    print("📥 Received from Torque:", data)

    try:
        rpm = float(data.get('rpm', 0))
        throttle = float(data.get('throttlepos', 0))
        coolant_temp = float(data.get('k9', 0))  # 'k9' is coolant temperature in Torque
    except ValueError:
        return "Invalid data format", 400

    payload = [{
        "RPM": rpm,
        "Throttle": throttle,
        "CoolantTemp": coolant_temp,
        "Timestamp": datetime.utcnow().isoformat()
    }]

    response = requests.post(POWER_BI_URL, json=payload)
    print("📤 Sent to Power BI:", payload)
    print("✅ Response code:", response.status_code)

    return "Data received"


if __name__ == '__main__':
    app.run(debug=True)
