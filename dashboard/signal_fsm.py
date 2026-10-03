# signal_fsm.py
import time

class TrafficSignalFSM:
    def __init__(self):
        # Define possible directions: North, South, East, West
        self.directions = ["North", "South", "East", "West"]
        self.current_direction_index = 0
        self.state = "GREEN"  # GREEN, YELLOW, RED, EMERGENCY_OVERRIDE
        self.active_direction = self.directions[self.current_direction_index]
        self.timer = 10  # Duration for current state in seconds
        self.last_update = time.time()

    def get_status(self):
        """Returns the current state dictionary for the dashboard and ESP32."""
        return {
            "active_direction": self.active_direction,
            "state": self.state,
            "timer": max(0, int(self.timer - (time.time() - self.last_update)))
        }

    def trigger_emergency(self, ambulance_direction):
        """Overrides normal cycle to give green light to the incoming ambulance."""
        self.state = "EMERGENCY_OVERRIDE"
        self.active_direction = ambulance_direction
        self.timer = 20  # Hold green for emergency clearance
        self.last_update = time.time()

    def update_cycle(self):
        """Standard round-robin traffic light cycle if no emergency is active."""
        if self.state == "EMERGENCY_OVERRIDE":
            # Let emergency override run out its timer
            if time.time() - self.last_update >= self.timer:
                self.state = "GREEN"
                self.last_update = time.time()
            return

        elapsed = time.time() - self.last_update
        if elapsed >= self.timer:
            # Cycle through states or directions
            if self.state == "GREEN":
                self.state = "YELLOW"
                self.timer = 3  # 3 seconds yellow
            elif self.state == "YELLOW":
                self.state = "RED"
                # Switch to next direction
                self.current_direction_index = (self.current_direction_index + 1) % len(self.directions)
                self.active_direction = self.directions[self.current_direction_index]
                self.timer = 10 # 10 seconds green for new direction
            elif self.state == "RED":
                self.state = "GREEN"
                self.timer = 10
            
            self.last_update = time.time()