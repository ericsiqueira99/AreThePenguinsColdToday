# py -m pip install tweepy
import tweepy
import random
import asyncio
import logging
import requests
import json, re, sys, argparse, os
from datetime import datetime  
from accuweather import (
    AccuWeather,
    ApiError,
    InvalidApiKeyError,
    InvalidCoordinatesError,
    RequestsExceededError,
)
from aiohttp import ClientError, ClientSession

dir_path = os.path.dirname(os.path.realpath(__file__))
temp_too_cold = -40
LOCATION_KEY = "2258520"
API_KEY = "dKH1I9ZCADE1qhcuEsYdEVlHFdQIwCF2"
too_cold_1 = ('Stay ', 'Keep ', 'Stand ')
too_cold_2 = ('warm, ', 'safe, ', 'strong, ', 'together, ')
too_cold_3 = ('little ', 'small ', 'chonky ', 'tuxedo wearing ', 'formal-chicken-looking ', 'fluffy ', 'faithful ', 'awkward walking ', 'woobly', 'artic')
too_cold_4 = ('folks', 'fellas', 'buddies', 'creatures', 'ones', 'friends', 'birds')
not_too_cold_1 = ('Enjoy the ', 'Have fun with the ')
not_too_cold_2 = ('sun, ', '"summer", ', 'cool weather, ', 'warm breeze, ', 'BBQ weather, ')

def getJSONfromUrl(url): 
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data

# connect to weather API and return temperature values in celcious and farenheit
def getTemperature():
    #get current weather by key
    url = f"http://dataservice.accuweather.com/currentconditions/v1/2258520?apikey="+API_KEY+"&details=true"
    json_data = getJSONfromUrl(url)
    unit_1 = "Metric" 
    unit_2 = "Imperial" 
    for p in json_data:
        current_temp_c=p["Temperature"][unit_1]
        current_temp_f=p["Temperature"][unit_2]
    result = (current_temp_c["Value"], current_temp_f["Value"])
    return result

# returns random generated coment about not being too cold 
def not_cold_comment():
    phrase_not_too_cold = not_too_cold_1[random.randrange(len(not_too_cold_1))] + not_too_cold_2[random.randrange(len(not_too_cold_2))]+ too_cold_3[random.randrange(len(too_cold_3))] +too_cold_4[random.randrange(len(too_cold_4))]+"!"
    return phrase_not_too_cold

# returns random generated coment about being too cold 
def cold_comment():
    phrase_too_cold = too_cold_1[random.randrange(len(too_cold_1))] + too_cold_2[random.randrange(len(too_cold_2))]+ too_cold_3[random.randrange(len(too_cold_3))] +too_cold_4[random.randrange(len(too_cold_4))]+"!"
    return phrase_too_cold    

# return string for tweet status, with temperature (both celcius and farenheit) and the random generated coment
def makeTweet():
    temperatures = getTemperature()
    temperature_c = temperatures[0]
    temperature_f = temperatures[1]
    if temperature_c < temp_too_cold:
        return "Yes! The current temperature in the south pole is " + str(temperature_c) + " ºC ("+ str(temperature_f)+" ºF).\nToday is too cold for some penguins.\n" + cold_comment()
    else:
        return "No! The current temperature in the south pole is " + str(temperature_c) + " ºC ("+ str(temperature_f)+" ºF).\nToday is not too cold for some penguins.\n" + not_cold_comment()

# return random image name from my folder that has not been used before
def getImage():
    with open('used_numbers.txt') as f:
        mylist = [tuple(map(int, i.split())) for i in f]
    #print(mylist[0])
    img_number = random.randrange(365)
    if mylist[0]:
        pass
    while img_number in mylist[0]:
        img_number = random.randrange(365)
    f = open('used_numbers.txt', 'a')     
    f.write(" %d" % img_number)
    f.close()
    image_path = dir_path+'\\simple_images\\penguins\\penguins_'
    print("Image used: %d" % img_number)
    return image_path+str(img_number)+".jpeg"

# connect to twitter API and post picture along with status
def tweetIt():
    twitter_auth_keys = {
        "consumer_key": "OnM4swn5C1ya2mQlKoh51bxce",
        "consumer_secret": "TjyInYKgMqJYa1NyXKOx2vnMeiZDHmNBmVh0xhSKBj0xbALkdD",
        "access_token": "1374480949262446602-zBySfLWb6li9pyAqD6gQIfoinZ4Zmk",
        "access_token_secret": "ZbMaj9j2HMIeFD833CUBd2RO5TxHJ46TDZfKvy4AeGlZG"
    }

    auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
    )
    auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
    )
    api = tweepy.API(auth)
    try:
        status = api.update_with_media(getImage(), status=makeTweet())
        print("All good!")
    except:
        print("Failed")     

if __name__ == "__main__":
    tweetIt()
    
    