"""
WeatherMe
SMS interfacing weather application for endeavors in areas with less than ideal cell service
@author: Simon Schonemann-Poppeliers
"""

from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests


def get_weather(lat, lon): #Scrapes weather.gov for lat/lon based weather. 
    url = 'https://forecast.weather.gov/MapClick.php?lat=' + str(lat) + '&lon=' + str(lon)
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all('td')
    basic_weather = []
    for item in data: #Cleans up weather data
        for i in item:
            i = (str(i).replace('</b>', '')).replace('<b>', '').replace('\n', '')
            basic_weather.append(i)
    weather = " ".join(basic_weather)
    print(weather)
    return weather


def get_lat(place):
    geolocator = Nominatim(user_agent="/avy")
    location = geolocator.geocode(place)
    lat = location.latitude
    return str(lat)


def get_lon(place):
    geolocator = Nominatim(user_agent="/avy")
    location = geolocator.geocode(place)
    lon = location.longitude
    return str(lon)


app = Flask(__name__) #Uses Flask, Twilio and Ngrok to create outward facing sms interface.


@app.route('/sms', methods=['GET', 'POST']) #Needs Ngrok to be running and configured with twilio to function.
def sms_reply():
    place = request.values.get('Body', None)
    print(place)
    lon = get_lon(place)
    lat = get_lat(place)
    weather = get_weather(lat, lon)

    resp = MessagingResponse()
    resp.message(weather)
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
    
    
