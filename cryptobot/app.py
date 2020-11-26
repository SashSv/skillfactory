import telebot
from config import keys, TOKEN
from extensions import APIException, Currency

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = """Чтобы начать работу введите:
<Имя валюты> <В какую валюту перевести> <Сумма>.
Чтобы увидеть список доступных валют введите команду\n /values"""
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for k in keys.keys():
        text = '\n'.join((text, k))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        text = Currency.get_price(message.text)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        bot.reply_to(message, text)

bot.polling(none_stop=True)