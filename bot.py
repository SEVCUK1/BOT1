# bot.py
import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "Привет! Я бот от Олега Шевчука. Используйте /help для получения информации.")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "Введите валюту в формате:\n валюта1(которую нужно перевести) валюта2(в какую валюту нужно перевести) количество  \n/values для списков валют.")

@bot.message_handler(commands=['values'])
def values_command(message):
    currencies = 'Доступные валюты:\nUSD\nEUR\nRUB'
    bot.reply_to(message, currencies)

@bot.message_handler(content_types=['text'])
def get_price(message):
    try:
        base, quote, amount = message.text.split()
        amount = float(amount)
        price = CurrencyConverter.get_price(base.upper(), quote.upper(), amount)
        text = f'{amount} {base.upper()} = {price} {quote.upper()}'
        bot.reply_to(message, text)
    except APIException as e:
        bot.reply_to(message, f'Ошибка: {str(e)}')
    except ValueError:
        bot.reply_to(message, 'Неправильный формат. Используйте: <валюта1> <валюта2> <количество>')
    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка: {str(e)}')

if __name__ == '__main__':
    bot.polling(none_stop=True)