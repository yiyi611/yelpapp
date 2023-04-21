# yelpapp
Ann Arbor Restaurant Guide


Description

This program provides a comprehensive introduction to restaurants in Ann Arbor. It uses the Yelp API to obtain restaurant data, including cuisine types, prices, ratings, and distances. The Google Maps API is used to get the longitude and latitude for each restaurant. The program is built using Flask, a Python web framework.

Users can interact with the web page to select their preferred restaurant in Ann Arbor. They can start by choosing the cuisine type they're interested in, and then select the restaurant ratings, prices, and distances in order of preference. The filtered results are displayed on the web page with detailed restaurant information. Each restaurant entry can be clicked on to open the corresponding Yelp page, where the user can access more detailed information.


Special Instructions

To run this program, you will need to have API keys for Yelp and Google Maps. You will need to replace the placeholders in the code with your own API keys.

To supply Yelp API key:
https://api.yelp.com/v3/businesses/search

To supply Google Maps API key: 
https://maps.googleapis.com/maps/api/geocode/json


Required Python Packages

The following Python packages are required to run this program:

flask

requests


How to Run the Program


1.Clone the repository to your local machine

2.Navigate to the project directory in your terminal

3.Set up your API keys as described above

4.Run the program by typing the following command in the terminal:python app.py

5.open a web browser and go to http://localhost:5000 to interact with the program

