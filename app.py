from geopy.geocoders import Nominatim
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests

'''
# Salut toi ! Besoin d'un tacos?
'''
#date and time
pickup_date = st.date_input(
    "Which day would you like to be picked up?")

pickup_time = st.time_input(
    "What time would you like to be picked up?")

#f'''{pickup_time}'''
pickup_datetime = str(pickup_date) + str(" ") + str(pickup_time)

#f'''{str(pickup_date)}'''
#f'''{str(pickup_time)}'''
#f'''{str(pickup_datetime)}'''
#pickup_datetime=pd.to_datetime(pickup_datetime)
#pickup and drop off on map

# @st.cache
# def get_map_data():
#     #print('get_map_data called')
#     return st.map(df)
#geolocator = Nominatim(user_agent="test")
#location_start = geolocator.geocode("175 5th Avenue NYC")


geolocator = Nominatim(user_agent="geoapiExercises")

#Needs to wait for text input before processing the next part of the code
#start_=str(st.text_input(label='Start Adress'))
#geocoded_str = geolocator.geocode(start_)

geocoded_str = geolocator.geocode("175 5th Avenue NYC")

#f'''{str(geocoded_str.latitude)}, {str(geocoded_str.longitude)}'''
#print(location.address)

pickup_latitude = str(geocoded_str.latitude)
pickup_longitude = str(geocoded_str.longitude)

geocoded_str_destination = geolocator.geocode("Museum of the Moving Image NYC")

dropoff_latitude = str(geocoded_str_destination.latitude)
dropoff_longitude = str(geocoded_str_destination.longitude)

# passenger count
passengers = st.slider('How many passengers?',1,8,2)

#API call using requests

url = 'https://taxifare.lewagon.ai/predict?'

#Let's build a dictionary containing the parameters for our API...
params = {
    'pickup_latitude': pickup_latitude,
    'pickup_longitude': pickup_longitude,
    'dropoff_latitude': dropoff_latitude,
    'dropoff_longitude': dropoff_longitude,
    'passenger_count': int(passengers),
    'pickup_datetime': pickup_datetime
    }

# Let's call our API using the `requests` package...

if st.button("Let's go !"):
    response = requests.get(url, params = params)
    # Let's retrieve the prediction from the **JSON** returned by the API...

    # ## Finally, we can display the prediction to the user
    df = pd.DataFrame(
        [(float(pickup_latitude),   float(pickup_longitude)), (float(dropoff_latitude),  float(dropoff_longitude))], columns=['latitude', 'longitude'])
    response_json=response.json()
    response_json_fare=response_json.get("fare")
    f"Your fare will cost around {round(response_json_fare,2)}"
    st.map(df)
