import datetime
import telebot
import requests
from bs4 import BeautifulSoup
import time
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
my_date = datetime.datetime.now()
month = (my_date.strftime("%B")).lower()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Привет!</b>', parse_mode='html')



@bot.message_handler(commands=['game'])
def game(message):

    url = f"https://vgtimes.ru/games/release-dates/nintendo-switch/sort-date/{month}-2022/"

    resp = requests.get(url)
    result = resp.content

    soup = BeautifulSoup(result, 'lxml')
    items = soup.find_all('div', class_='game_search')
    conunter = 0
    for item in reversed(items):
        conunter += 1
        name_game = item.find('div', class_='title').get_text()
        link_game = item.find('a').get('href')
        date_release = item.find('div', class_='date date_highlight').get_text()
        result = f'{conunter}) {name_game} - https://vgtimes.ru/{link_game}\nДата выхода: {date_release}\n'
        bot.send_message(message.chat.id, f'{result}', parse_mode='html')
        time.sleep(1)
        if conunter == 5:
            break

    return result


bot.polling(none_stop=True)