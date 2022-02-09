import telebot
from random import randint

answer_list = [
    "i don't understand",
    "дичь какая-то, напиши нормально",
    "Введите пин от карты универсальная:",
    "түшүнбөй жатам",
    "我不明白",
    "заказ оформлен! ТТН 228228228",
    "вжух и ты питух",
    "не понял тебя",
    "шо ты пишешь, дядя...",
    "камри 3.5 уууууу японцы делают вещи",
    "вы сломали бота",
    "бот не бот"
]

length = len(answer_list) - 1

bot = telebot.TeleBot('5197977358:AAHtKsuUAoDRTyTBUhG9pJYidtCwJyEIR4k')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Привет, я сын питона. Напиши мне 'привет'.")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    random_answer = answer_list[randint(0, length)]
    print(message.chat.id)
    print(f'user: {message.text}')
    if message.text == "привет":
        bot.send_message(message.chat.id, 'здарова, че хотел?')
        print('bot: здарова, че хотел?')
    else:
        bot.send_message(message.chat.id, random_answer)
        print(f'bot: {random_answer}')

bot.polling(none_stop=True, interval=0)
