from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

API_KEY = "AIzaSyBaTU1KYeAn_qbL3JQBlDBaHD2XKjHbm48"
YELP_API_KEY = "VH-UIMZ42KSB7DzvE5Z8hoIgu_aiFxy3S-X2SDRedjHIvKfitkMD3wGeYt86fqX-n3q4C2x6EZUHckOdAviJUtgNfSt2MGz9V5y_IQvPQGg8f9tjEXL7Y7sPEpZBZHYx"

# Function to get restaurant data from Yelp API
def get_restaurants(location, categories):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}"
    }
    params = {
        "location": location,
        "categories": categories,
        "sort_by": "rating"
    }
    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)
    return data["businesses"]

# Function to get restaurant latitude and longitude from Google Maps API
def get_lat_lng(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    lat = data["results"][0]["geometry"]["location"]["lat"]
    lng = data["results"][0]["geometry"]["location"]["lng"]
    return (lat, lng)

# Homepage
@app.route("/")
def home():
    return render_template("home.html")

# Restaurant search page
@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        location = request.form["location"]
        cuisine = request.form.getlist("cuisine")
        categories = ",".join(cuisine)
        restaurants = get_restaurants(location, categories)
        for restaurant in restaurants:
            address = restaurant["location"]["address1"] + ", " + restaurant["location"]["city"] + ", " + restaurant["location"]["state"] + " " + restaurant["location"]["zip_code"]
            lat, lng = get_lat_lng(address)
            restaurant["latitude"] = lat
            restaurant["longitude"] = lng
        return render_template("search.html", restaurants=restaurants)
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
