# server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Shared storage for the latest incoming data
latest_ambulance_data = {
    "direction": "North",
    "distance": 100.0,
    "speed": 0.0,
    "active": False
}

latest_junction_state = {
    "active_direction": "North",
    "state": "GREEN",
    "timer": 10
}

@app.route('/ambulance-data', methods=['POST'])
def receive_ambulance_data():
    """Endpoint where the Ambulance ESP32 sends its live data."""
    global latest_ambulance_data
    data = request.json
    if data:
        latest_ambulance_data = {
            "direction": data.get("direction", "North"),
            "distance": float(data.get("distance", 100.0)),
            "speed": float(data.get("speed", 0.0)),
            "active": bool(data.get("active", True))
        }
        return jsonify({"status": "success", "message": "Data received successfully"}), 200
    return jsonify({"status": "error", "message": "No data provided"}), 400

@app.route('/ambulance-data', methods=['GET'])
def get_ambulance_data():
    """Allows engine.py or dashboard to read the latest ambulance data."""
    return jsonify(latest_ambulance_data), 200

@app.route('/junction-state', methods=['POST'])
def update_junction_state():
    """Endpoint for engine.py to update what the junction should display."""
    global latest_junction_state
    data = request.json
    if data:
        latest_junction_state = {
            "active_direction": data.get("active_direction", "North"),
            "state": data.get("state", "GREEN"),
            "timer": int(data.get("timer", 10))
        }
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/junction-state', methods=['GET'])
def get_junction_state():
    """Endpoint where the Junction ESP32 or Dashboard reads the current signal state."""
    return jsonify(latest_junction_state), 200

if __name__ == '__main__':
    # Run server locally on port 5000, accessible via your laptop's local network IP
    app.run(host='0.0.0.0', port=5000, debug=True)