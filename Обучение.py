import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def hello_user(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! '
                                      f'Моя задача конвертировать валюты в зависимости от того, какая тебе требуется! '
                                      f'Введи название валюты, потом название той, в которую хочешь конвертировать и количество. '
                                      f'Например: Доллар рубль 100. '
                                      f'Увидеть список доступных валют можно командой /values.')

@bot.message_handler(commands = ['help'])
def hello_user(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Чтобы начать работу введи запрос в следующем формате:\n'
                                      f'<название валюты><название валюты в которую хочешь перевести><количество переводимой валюты>. \n'
                                      f'Увидеть список доступных валют можно с помощью команды: /values.')

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionExeption('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка ввода\n{e}.')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}.')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling()