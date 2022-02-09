import telebot
from random import randint

answer_list = [
    "i don't understand this language",
    "не разумею",
    "no lo entiendo",
    "түшүнбөй жатам",
    "我不明白",
    "nerozumím",
    "jeg forstår ikke",
    "не понял тебя"
]


bot = telebot.TeleBot('5197977358:AAHtKsuUAoDRTyTBUhG9pJYidtCwJyEIR4k')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Привет, я сын питона. Напиши мне 'привет'.")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(message.text)
    if message.text == "привет":
        bot.send_message(message.chat.id, 'здарова, че хотел?')
    else:
        bot.send_message(message.chat.id, answer_list[randint(0, 7)])

bot.polling(none_stop=True, interval=0)
