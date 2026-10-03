# logic.py

def calculate_eta(distance_meters, speed_mps):
    """
    Calculates the Estimated Time of Arrival (ETA) in seconds.
    distance_meters: distance of ambulance from junction in meters
    speed_mps: speed of ambulance in meters per second
    """
    if speed_mps <= 0:
        return 9999.0  # Infinite/very high time if stationary or invalid speed
    
    eta = distance_meters / speed_mps
    return round(eta, 2)


def should_trigger_priority(eta, threshold_seconds=30.0):
    """
    Determines if the ambulance is close enough to trigger emergency green override.
    threshold_seconds: Default is 30 seconds away.
    """
    return eta <= threshold_seconds


def calculate_clearance_time(queue_count):
    """
    Calculates how long the green light needs to stay active 
    based on the number of vehicles waiting in the queue.
    Assuming roughly 2 seconds per vehicle to clear.
    """
    base_time = 5  # minimum clearance buffer
    time_per_vehicle = 2.0
    return int(base_time + (queue_count * time_per_vehicle))