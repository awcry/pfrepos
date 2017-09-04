
import config # main config with token
import telebot

from selenium import webdriver
from PIL import Image

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Добро пожаловать!')

@bot.message_handler(commands=['rasp'])
def send_photo(message):
    photo_rasp = open('rasp.png', 'rb')
    bot.send_photo(message.chat.id, photo_rasp)

@bot.message_handler(commands=['changes'])    
def send_photo_changes(message):
    bot.send_message(message.chat.id, 'Подождите пару секунд..')
    photo_part1 = open('changes_part1.png', 'rb')
    bot.send_photo(message.chat.id, photo_part1)
    photo_part2 = open('changes_part2.png', 'rb')
    bot.send_photo(message.chat.id, photo_part2)
    
@bot.message_handler(commands=['scriptupdate'])
def scriptupdate(message):
    bot.send_message(message.chat.id, 'Выполняется обновление..')
    driver = webdriver.PhantomJS()
    driver.set_window_size(800, 600)
    driver.get(config.url) # url changes
    driver.save_screenshot('changes.png')
    changes_im = Image.open('changes.png')
    (width, height) = changes_im.size
    frame = changes_im.crop(((310, 696, 1008, height - 550)))
    frame.save('changes_frame.png')
    changes_im1 = Image.open('changes_frame.png')
    (width_frame, height_frame) = changes_im1.size
    part1 = changes_im1.crop(((0, 0, width_frame, 1231)))
    part1.save('changes_part1.png')
    changes_im2 = Image.open('changes_frame.png')
    part2 = changes_im2.crop(((0, 1231, width_frame, height_frame)))
    part2.save('changes_part2.png')
    bot.send_message(message.chat.id, 'Успешно!')
    
if __name__ == '__main__':
     bot.polling(none_stop=True)


