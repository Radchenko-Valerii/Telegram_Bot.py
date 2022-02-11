import telebot
import json
import requests
from geopy import geocoders
import constants
import emoji
from telebot import types


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
    dict_weather['now'] = {'temp': json_data[0]['Temperature']['Value'], 'unit': json_data[0]['Temperature']['Unit'],
                           'icon': json_data[0]['WeatherIcon'], 'sky': json_data[0]['IconPhrase']}
    for i in range(1, len(json_data)):
        time = 'after' + str(i) + 'h'
        dict_weather[time] = {'temp': json_data[i]['Temperature']['Value'], 'unit': json_data[i]['Temperature']['Unit'],
                              'icon': json_data[i]['WeatherIcon'], 'sky': json_data[i]['IconPhrase']}
    return dict_weather


bot = telebot.TeleBot(constants.TOKEN_BOT_API)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(m.chat.id, "Привет, я сын питона. Напиши мне любой город и я скину тебе погоду сейчас.", reply_markup=a)


weater_info = []


@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        print(message.chat.id)
        print(f'user: {message.text}')
        geo = geo_pos(message.text)
        code = code_location(geo, constants.TOKEN_WEATER_API)
        res = weather(code, constants.TOKEN_WEATER_API)
        weater_info.append(res)
        temp = res["now"]["temp"]
        sky = res["now"]["sky"].lower()
        unit = res["now"]["unit"]
        print(f'сейчас {temp}, {sky}')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(2, 12, 2):
            item = types.KeyboardButton(f"погода в течении {i} часов")
            markup.add(item)
        bot.send_message(message.chat.id, f'{emoji.weater_emodji[res["now"]["icon"]]} Сейчас {temp} {unit}, {sky}',
                         reply_markup=markup)
        bot.register_next_step_handler(message, handle_text2);
    except AttributeError as error:
        print(error)
        bot.send_message(message.chat.id, 'Населенный пункт не найден')


def handle_text2(message):
    try:
        if message.text == 'погода в течении 2 часов':
            answer = weater_info[0]["after2h"]
        elif message.text == 'погода в течении 4 часов':
            answer = weater_info[0]["after4h"]
        elif message.text == 'погода в течении 6 часов':
            answer = weater_info[0]["after6h"]
        elif message.text == 'погода в течении 8 часов':
            answer = weater_info[0]["after8h"]
        elif message.text == 'погода в течении 10 часов':
            answer = weater_info[0]["after10h"]

        bot.send_message(message.chat.id, f'{emoji.weater_emodji[answer["icon"]]} Будет {answer["sky"].lower()}, {answer["temp"]} {answer["unit"]}. Введите другой населенный пункт')
    except UnboundLocalError as error:
        print(error)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        reboot = types.KeyboardButton("/start")
        markup.add(reboot)
        bot.send_message(message.chat.id, 'Неизвестная инструкция', reply_markup=markup)


bot.polling(none_stop=True, interval=0)
