
import config
import telebot

from selenium import webdriver
from PIL import Image

bot = telebot.TeleBot(config.token)

#@bot.message_handler(content_types=["text"])
#def repeat_all_messages(message): 
    #bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['rasp'])
def send_photo(message):
    photo_rasp = open('/tmp/rasp.png', 'rb')
    bot.send_photo(message.chat.id, photo_rasp)

@bot.message_handler(commands=['changes'])    
def send_photo_changes(message):
    bot.send_message(message.chat.id, 'Подождите пару секунд..')
    driver = webdriver.PhantomJS()
    driver.set_window_size(800, 600)
    driver.get('http://pgups-karelia.ru/edu-process/change-ochno-spo/')
    driver.save_screenshot('/tmp/changes.png')
    changes_im = Image.open('/tmp/changes.png')
    (width, height) = changes_im.size
    frame = changes_im.crop(((310, 696, 1008, height - 550)))
    frame.save('/tmp/changes_frame.png')
    changes_im1 = Image.open('/tmp/changes_frame.png')
    (width_frame, height_frame) = changes_im1.size
    part1 = changes_im1.crop(((0, 0, width_frame, 1231)))
    part1.save('/tmp/changes_part1.png')
    changes_im2 = Image.open('/tmp/changes_frame.png')
    part2 = changes_im2.crop(((0, 1231, width_frame, height_frame)))
    part2.save('/tmp/changes_part2.png')
    photo_part1 = open('/tmp/changes_part1.png', 'rb')
    bot.send_photo(message.chat.id, photo_part1)
    photo_part2 = open('/tmp/changes_part2.png', 'rb')
    bot.send_photo(message.chat.id, photo_part2)
    
if __name__ == '__main__':
     bot.polling(none_stop=True)


