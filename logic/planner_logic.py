from config import DESTINATION_FILE
from logic.utils import load_json, days_between
from logic.weather_logic import get_weather, get_recommended_categories



# travel style based on number
STYLE_SLOTS={
    "Relaxed":2,"Balanced":3,"Packed":4
}


# time slots 
TIME_SLOTS={
    "Morning","Afternoon","Evening","Night"
}




# for getting destination data
# returns a dictionary of destination data
# if the destination is not found, returns an empty dictionary
def get_destination_data(destination_name):
    all_destinations = load_json(DESTINATIONS_FILE)
    return all_destinations.get(destination_name)





# for scoring attractions based on interests and recommended categories
# returns a score between 0 and 5
def _score_attraction(attraction, interests, recommended_categories):
    score = 0
    attraction_type = attraction.get("type", "")

    if attraction_type in interests:
        score += 3
    if attraction_type in recommended_categories:
        score += 2
    return score





# for generating itinerary
# returns a dictionary of itinerary data
# if the destination is not found, returns an empty dictionary
def generate_itinerary(destination, start_date, end_date, budget, interests,
                        transport, travel_style):
    dest_data = get_destination_data(destination)
    if not dest_data:
        return {"error": f"No data found for destination '{destination}'."}

    num_days = days_between(start_date, end_date)
    weather = get_weather(destination, dest_data.get("lat"), dest_data.get("lon"))
    recommended_categories = get_recommended_categories(weather)

    attractions = dest_data.get("attractions", [])
    scored = sorted(
        enumerate(attractions),
        key=lambda pair: (-_score_attraction(pair[1], interests, recommended_categories), pair[0])
    )
    ranked_attractions = [a for _, a in scored]

    slots_per_day = STYLE_SLOTS.get(travel_style, 3)
    time_labels = TIME_SLOTS[:slots_per_day]

    days = []
    total_cost = 0
    attraction_cursor = 0
    num_attractions = len(ranked_attractions)

    # Base transport cost per day, simulated
    transport_cost_per_day = {
        "Walking": 0,
        "Public Transport": 150,
        "Taxi": 600,
        "Rental Car": 1200,
        "Shared Taxi Pool": 300,
    }.get(transport, 200)

    for day_index in range(num_days):
        day_plan = {"day": day_index + 1, "slots": [], "day_cost": 0}

        for label in time_labels:
            if num_attractions == 0:
                break
            attraction = ranked_attractions[attraction_cursor % num_attractions]
            attraction_cursor += 1

            cost = attraction.get("cost", 0)
            day_plan["slots"].append({
                "time": label,
                "activity": attraction.get("name"),
                "type": attraction.get("type"),
                "cost": cost,
            })
            day_plan["day_cost"] += cost

        day_plan["day_cost"] += transport_cost_per_day
        day_plan["transport_cost"] = transport_cost_per_day
        total_cost += day_plan["day_cost"]
        days.append(day_plan)

    budget_val = budget or 0
    over_budget = budget_val > 0 and total_cost > budget_val
    budget_difference = round(total_cost - budget_val, 2) if budget_val else 0

    return {
        "destination": destination,
        "description": dest_data.get("description"),
        "category": dest_data.get("category"),
        "coordinates": {"lat": dest_data.get("lat"), "lon": dest_data.get("lon")},
        "hotel": dest_data.get("hotel"),
        "num_days": num_days,
        "start_date": start_date,
        "end_date": end_date,
        "travel_style": travel_style,
        "transport": transport,
        "interests": interests,
        "weather": weather,
        "recommended_categories": recommended_categories,
        "days": days,
        "total_estimated_cost": round(total_cost, 2),
        "budget": budget_val,
        "over_budget": over_budget,
        "budget_difference": abs(budget_difference) if over_budget else 0,
    }





# for getting a summary of all destinations
# returns a list of dictionaries, each containing destination name, description, category, latitude, longitude
def get_all_destinations_summary():
    all_destinations = load_json(DESTINATIONS_FILE)
    summary = []
    for name, data in all_destinations.items():
        summary.append({
            "name": name,
            "description": data.get("description"),
            "category": data.get("category"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
        })
    return summary
