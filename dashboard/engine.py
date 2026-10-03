# engine.py
import time
import requests
from logic import calculate_eta, should_trigger_priority, calculate_clearance_time
from signal_fsm import TrafficSignalFSM

# URL of the local Flask server we just built
SERVER_URL = "http://127.0.0.1:5000"

def main():
    print("Starting Smart Signal Engine Hub...")
    fsm = TrafficSignalFSM()
    
    while True:
        try:
            # 1. Fetch latest data from server (sent by Ambulance ESP32 or Simulator)
            response = requests.get(f"{SERVER_URL}/ambulance-data", timeout=2)
            if response.status_code == 200:
                amb_data = response.json()
                
                direction = amb_data.get("direction", "North")
                distance = amb_data.get("distance", 100.0)
                speed = amb_data.get("speed", 0.0)
                is_active = amb_data.get("active", False)
                
                # 2. Run calculations from logic.py
                eta = calculate_eta(distance, speed)
                trigger = should_trigger_priority(eta, threshold_seconds=30.0)
                
                if is_active and trigger:
                    print(f"EMERGENCY! Ambulance approaching from {direction} | ETA: {eta}s")
                    fsm.trigger_emergency(direction)
                else:
                    # Run regular round-robin cycle
                    fsm.update_cycle()
            
            # 3. Push current state back to server so Junction ESP32 / Dashboard can read it
            current_state = fsm.get_status()
            requests.post(f"{SERVER_URL}/junction-state", json=current_state, timeout=2)
            
        except Exception as e:
            print(f"Engine loop error (is server.py running?): {e}")
            
        # Run the loop every 1 second
        time.sleep(1.0)

if __name__ == "__main__":
    main()