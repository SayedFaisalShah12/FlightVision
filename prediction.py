def predict_landing_time(distance_km, speed_kmh):
    """
    Returns ETA in minutes
    """
    if speed_kmh <= 0:
        return None
    time_hours = distance_km / speed_kmh
    return round(time_hours * 60, 2)
