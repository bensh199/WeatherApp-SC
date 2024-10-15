from pymongo import MongoClient
import requests
import json
from weather import *
import datetime

MONGO_URI = f'mongodb://admin:admin@172.17.0.1:27017/'
DB_NAME = 'data'
COLLECTION_NAME = 'weather'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# function to query the mongodb weather collection for a document with a matching city
def query_for_data(city: str):
    current_time = datetime.datetime.now().strftime("%H:%M")
    
    if collection.find_one({"city": city}) != None and abs(datetime.datetime.strptime(current_time, "%H:%M") - datetime.datetime.strptime(collection.find_one({"city": "Tel Aviv"})["timestamp"], "%H:%M")) < datetime.timedelta(minutes=1):
        return collection.find_one({"city": city})
    else:
        return update_mogodb(city)
def update_mogodb(city):

    return add_weather_data(get_weather_data(city))

# Function to add a purchase to MongoDB
def add_weather_data(data: dict):
    
    weather_data = {
        'timestamp': datetime.datetime.now().strftime("%H:%M"),
        'city': data['city'],
        'country': data['country'],
        'current_temp': data['current_temp'],
        'current_humidity': data['current_humidity'],
        'date': data['date_stamp'],
        'week_day': data['week_day'],
        'daily_max_temps': data['daily_max_temps'],
        'daily_min_temps': data['daily_min_temps'],
        'humidity': data['humidity']
    }

    if collection.find_one({"city": weather_data['city']}) != None:
        print("1")
        collection.update_one({"city": weather_data['city']}, {"$set": weather_data})
        return data
    else:
        collection.insert_one(weather_data)
        print("2")
        return data

if __name__ == '__main__':
    # update_mogodb("Ashdod")
    # print(get_timestamp())
    # print(type(get_weather_data("Tel Aviv")))
    print(query_for_data("Tel Aviv"))
    # print(type(datetime.datetime.strptime(collection.find_one({"city": "Tel Aviv"})["timestamp"], "%H:%M")))
    # current_time = datetime.datetime.now().strftime("%H:%M")
    # print(abs(datetime.datetime.strptime(current_time, "%H:%M") - datetime.datetime.strptime(collection.find_one({"city": "Tel Aviv"})["timestamp"], "%H:%M")))
    # print(datetime.datetime.now().time().replace(second=0, microsecond=0))
    # print(add_weather_data(get_weather_data("Tel Aviv")))
    pass