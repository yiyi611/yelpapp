from flask import Flask, render_template, request
import requests
from collections import defaultdict

app = Flask(__name__)

# Yelp API credentials
YELP_API_KEY = "VH-UIMZ42KSB7DzvE5Z8hoIgu_aiFxy3S-X2SDRedjHIvKfitkMD3wGeYt86fqX-n3q4C2x6EZUHckOdAviJUtgNfSt2MGz9V5y_IQvPQGg8f9tjEXL7Y7sPEpZBZHYx"
YELP_HEADERS = {
    "Authorization": f"Bearer {YELP_API_KEY}"
}

# Google Maps API credentials
GOOGLE_API_KEY = "AIzaSyBaTU1KYeAn_qbL3JQBlDBaHD2XKjHbm48"

# Yelp API endpoint
YELP_URL = "https://api.yelp.com/v3/businesses/search"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    # Retrieve the user's selection from the form
    cuisine = request.form.get("cuisine")
    price = request.form.get("price")
    rating = request.form.get("rating")
    distance = request.form.get("distance")

    # Yelp API parameters
    params = {
        "location": "Ann Arbor",
        "categories": "restaurants",
        "sort_by": f"{rating},distance,price",
        "price": price,
    }

    # Send the request to the Yelp API
    response = requests.get(YELP_URL, headers=YELP_HEADERS, params=params).json()

    # Parse the response and retrieve the restaurant data
    businesses = response["businesses"]

    # Filter the restaurants based on the user's selection of cuisine type
    if cuisine != "all":
        businesses = [business for business in businesses if cuisine in [category["title"].lower() for category in business["categories"]]]

    # Create a nested dictionary to organize the restaurants by cuisine type
    restaurants_by_cuisine = defaultdict(lambda: defaultdict(list))
    for business in businesses:
        name = business["name"]
        cuisine = ", ".join(business["categories"][i]["title"] for i in range(len(business["categories"])))
        price = business.get("price", "N/A")
        rating = business["rating"]
        distance = round(business["distance"] / 1609.34, 2) # Convert meters to miles
        location = f"{business['location']['address1']}, {business['location']['city']}, {business['location']['state']} {business['location']['zip_code']}"
        
        # Retrieve the latitude and longitude of the restaurant using the Google Maps API
        google_url = "https://maps.googleapis.com/maps/api/geocode/json"
        google_params = {
            "address": location,
            "key": GOOGLE_API_KEY
        }
        google_response = requests.get(google_url, params=google_params).json()
        latitude = google_response["results"][0]["geometry"]["location"]["lat"]
        longitude = google_response["results"][0]["geometry"]["location"]["lng"]

        # Add the restaurant data to the nested dictionary
        restaurants_by_cuisine[cuisine]["name"].append(name)
        restaurants_by_cuisine[cuisine]["price"].append(price)
        restaurants_by_cuisine[cuisine]["rating"].append(rating)
        restaurants_by_cuisine[cuisine]["distance"].append(distance)
        restaurants_by_cuisine[cuisine]["location"].append(location)
        restaurants_by_cuisine[cuisine]["latitude"].append(latitude)
        restaurants_by_cuisine[cuisine]["longitude"].append(longitude)

    # Sort the restaurants based on the user's selection of rating and distance
    for cuisine, restaurants in restaurants_by_cuisine.items():
        if rating == "rating_high":
            restaurants["name"], restaurants["price"], restaurants["distance"], restaurants

if __name__ == '__main__':
    print('starting Flask app', app.name)
    app.run(debug=True)