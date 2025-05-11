from flask import Flask, request
import requests

app = Flask(__name__)

POWERBI_URL = "https://api.powerbi.com/beta/b4c6b754-54e3-41e4-a8da-304355c62816/datasets/34fe22e9-4150-4f54-8141-63905227d0c6/rows?experience=power-bi&key=zFkMSWchr%2BhtgyD2nWHXTa4DyRO0CcSWACy7eFi6YXCUsyIkNravbBbEAJ9Jlw7Yg0xXRsjgpKbh4M4HIpLT6Q%3D%3D"

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("Received data:", data)
    try:
        response = requests.post(POWERBI_URL, json=[data])
        return {"status": "sent to Power BI", "response": response.text}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/')
def home():
    return 'Flask server is running!'
