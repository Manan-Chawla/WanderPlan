import json
import math
from datetime import datetime



# for loading json files
def load_json(filepath):
    try:
        with open(filepath,"r",encoding="utf-8") as f:
            return json.load(f)
    except(FileNotFoundError,json.JSONDecoderError):
        return {}

# for saving json files
def save_json(filepath,data):
    with open(filepath,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4)




# for calculating distance between two points on earth
# using haversine formula (actually use by the uber and ola apps)
# returns distance in km
def haversine_distance(lat1, lon1, lat2, lon2):
    R=6371 # radius of earth in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (math.sin(d_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c



# for calculating number of days between two dates
# returns number of days between two dates, including the start date
# if the start date is after the end date, returns 0
def days_between(start_date_str, end_date_str):
    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d")
        end = datetime.strptime(end_date_str, "%Y-%m-%d")
        delta = (end - start).days + 1
        return max(delta, 1)
    except (ValueError, TypeError):
        return 1



# for calculating time difference between two times
# returns time difference in minutes
# if the second time is before the first time, returns negative time difference
# if the first time is after the second time, returns 0
def time_diff_minutes(time_str_a, time_str_b):
    try:
        fmt = "%H:%M"
        t1 = datetime.strptime(time_str_a, fmt)
        t2 = datetime.strptime(time_str_b, fmt)
        diff = abs((t1 - t2).total_seconds()) / 60
        return diff
    except (ValueError, TypeError):
        return float("inf")