import streamlit as st
import datetime
import requests
import pandas as pd
import base64
import numpy as np

@st.cache
def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def image_tag(path):
    encoded = load_image(path)
    tag = f'<img src="data:image/png;base64,{encoded}">'
    return tag

def background_image_style(path):
    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    '''
    return style

'''
# Fi's Taxi Fare Model
'''

st.markdown("""Get to your destination on time""")

date = st.date_input("Enter the date you would like to travel:", value=datetime.datetime.today())
time = st.time_input("and your desired time:", value=datetime.datetime.now())
final_datetime = datetime.datetime.combine(date, time)

p_longitude = st.number_input('Insert a pickup longitude:', min_value=float(-180.0000), format="%0.7f")
p_latitude = st.number_input('Insert a pickup latitude:', key='pickup_lat', min_value=float(-180.0000), format="%0.7f")
d_longitude = st.number_input('Insert a dropoff longitude:', key='dropoff_long', min_value=float(-180.0000), format="%0.7f")
d_latitude = st.number_input('Insert a dropoff latitude:', key='dropoff_lat', min_value=float(-180.0000), format="%0.7f")

passenger_count = st.number_input('How many passengers:', key='pass_count', min_value=int(0))


## calling api section
params = {'pickup_datetime' : final_datetime,
        'pickup_longitude' : p_longitude,
        'pickup_latitude' : p_latitude,
        'dropoff_longitude' : d_longitude,
        'dropoff_latitude' : d_latitude,
        'passenger_count' : passenger_count
        }

url = 'https://taxifare.lewagon.ai/predict'
response = requests.get(url, params=params)
fare_amount = response.json()['fare']

if st.button('estimate your fare:'):
    st.metric("The total fare amount is: ", f'{fare_amount:.2f}')
    st.balloons()

map_data = pd.DataFrame({
    'latitude': [p_latitude, d_latitude],
    'longitude': [p_longitude, d_longitude]
})

## Create a map with the data
st.map(map_data, zoom=10)

# image_path = './nyc_taxi.jpg'
# st.write(background_image_style(image_path), unsafe_allow_html=True)
