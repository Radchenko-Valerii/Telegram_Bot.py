import telebot
import constants
import requests
import json

bot = telebot.TeleBot(constants.TOKEN_BOT_API_G2)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Привет, я помогу тебе найти прикольную гифку. Напиши мне слово/реплику и я отправлю её тебе.")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        print(message.chat.id)
        print(f'user: {message.text}')
        url = f'https://api.giphy.com/v1/gifs/search?api_key={constants.TOKEN_GIPHY_API}&q={message.text}&limit=3&offset=0&rating=g&lang=ru'
        response = requests.get(url)
        json_data = json.loads(response.text)
        print(json_data)
        answer = json_data["data"][0]["images"]["original"]["url"]
        print(json_data["data"][0]["images"]["original"]["url"])
        bot.send_message(message.chat.id, "Держи \U0001F60E")
        bot.send_animation(message.chat.id, answer)
    except Exception as error:
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте позже или измените запрос \U0001F97A")
        print(error)


bot.polling(none_stop=True, interval=0)
