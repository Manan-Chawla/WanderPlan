# **WanderPlan — Dynamic Itinerary Planner**

A full-stack college project built with **Flask**, **Bootstrap 5**, **Leaflet.js/OpenStreetMap**, and the **OpenWeatherMap API**. It generates smart, day-wise travel itineraries across 9 Indian destinations that adapt to live weather, simulated safety alerts, budget, and personal travel style — plus a simulated taxi-pooling matcher.
No login/registration, no external database — everything runs on local JSON files.


## **How to run locally?**

1. Install python and pip
2. create a folder
3. Create a Virtual Enviorment
4. Activate Virtual Enviorment
5. Install Dependencies
6. Add Openweathermap API key
7. Run app using : python app.py
8. Open : localhost :5000


## **Key Features**

| Feature | Description |
|---|---|
| **Smart Planner** | Generates a day-wise itinerary (Morning/Afternoon/Evening) based on destination, dates, budget, interests, transport, and travel style. |
| **Live Weather Sync** | Pulls real-time weather from OpenWeatherMap; rainy conditions automatically shift recommendations toward museums/shopping/restaurants, clear weather favors outdoor spots. |
| **Safety Dashboard** | Reads `alerts.json` to display Safe / Warning / Danger status per destination. |
| **Interactive Map** | Leaflet.js + OpenStreetMap showing destination markers, hotel markers, and simulated travel routes (polylines) since no routing API is used. |
| **Taxi Pool Matcher** | Matches the user against sample travelers in `travelers.json` heading to the same destination within a 20-minute window, then estimates shared savings and CO₂ reduction. |



## **Tech Stack**

- **Frontend:** HTML5, CSS3 (Glassmorphism + gradients), Vanilla JS, Bootstrap 5, Google Fonts (Poppins), Font Awesome
- **Backend:** Python Flask
- **Maps:** Leaflet.js + OpenStreetMap tiles
- **Weather:** OpenWeatherMap API
- **Data storage:** Local JSON files (no MongoDB/MySQL/PostgreSQL)
- **Auth:** None (by design — no login/registration)
