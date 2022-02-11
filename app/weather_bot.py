from lib2to3.pgen2 import token
from re import I
import telebot
import json
import requests
from geopy import geocoders
from os import environ
import constants


def geo_pos(city: str):
  geolocator = geocoders.Nominatim(user_agent="telebot")
  latitude = str(geolocator.geocode(city).latitude)
  longitude = str(geolocator.geocode(city).longitude)
  return [latitude, longitude]

def code_location(coordinates_array, api_token: str):
  url_location_key = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_token}&q={coordinates_array[0]},{coordinates_array[1]}&language=ru'
  res_loc = requests.get(url_location_key, headers={"APIKey": api_token})
  json_data = json.loads(res_loc.text)
  code = json_data['Key']
  return code
  
def weather(cod_loc: str, token_accu: str):
  url_weather = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{cod_loc}?apikey={token_accu}&language=ru&metric=True'
  response = requests.get(url_weather, headers={"APIKey": token_accu})
  json_data = json.loads(response.text)
  dict_weather = dict()
  dict_weather['link'] = json_data[0]['MobileLink']
  dict_weather['now'] = {'temp': json_data[0]['Temperature']['Value'], 'sky': json_data[0]['IconPhrase']}
  for i in range(len(json_data), 1):
    time = 'after' + str(i) + 'h'
    dict_weather[time] = {'temp': json_data[i]['Temperature']['Value'], 'sky': json_data[i]['IconPhrase']}
  return dict_weather

# geo = geo_pos('Запорожье')
# code = code_location(geo, constants.TOKEN_WEATER_API)
# print(weather(code, constants.TOKEN_WEATER_API))

bot = telebot.TeleBot(constants.TOKEN_BOT_API)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Привет, я сын питона. Напиши мне любой город и я скину тебе погоду сейчас.")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    
    print(message.chat.id)
    print(f'user: {message.text}')
    geo = geo_pos(message.text)
    code = code_location(geo, constants.TOKEN_WEATER_API)
    res = weather(code, constants.TOKEN_WEATER_API)
    print(res)
    bot.send_message(message.chat.id, f'сейчас +{res["now"]["temp"]} по цельсию, {res["now"]["sky"]}')
    print(f'сейчас {res["now"]["temp"]}, {res["now"]["sky"]}')
    

bot.polling(none_stop=True, interval=0)


