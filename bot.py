#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config              # main config with token
import telebot
from telebot import types  # inline types
import urllib
import socket

from selenium import webdriver
from PIL import Image

bot = telebot.TeleBot(config.token)
    
@bot.message_handler(commands=['start'])
def start_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(config.markup_1) 
    markup.add(config.markup_2)
    username = message.from_user.first_name
    msg = bot.send_message(message.chat.id, username + ', что вам показать?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step_menu)

def process_step_menu(message):
    chat_id = message.chat.id
    if message.text == config.markup_1 or message.text == 'Изменения' or message.text == 'изменения':
        try:
            changes_im = Image.open(config.chng_file)
            (width, height) = changes_im.size
            frame = changes_im.crop((310, 696, 1008, height - 550))
            frame.save(config.chng_frame)
            changes_im1 = Image.open(config.chng_frame)
            (width_frame, height_frame) = changes_im1.size
            part1 = changes_im1.crop((0, 0, width_frame, 1231))
            part1.save(config.chng_part1)
            changes_im2 = Image.open(config.chng_frame)
            part2 = changes_im2.crop((0, 1231, width_frame, height_frame))
            part2.save(config.chng_part2)
            photo_part1 = open(config.chng_part1, 'rb')
            bot.send_photo(message.chat.id, photo_part1)
            photo_part2 = open(config.chng_part2, 'rb')
            bot.send_photo(message.chat.id, photo_part2)
            print('User: ' + str(message.chat.id) + '@' + str(message.from_user.first_name) + str(message.from_user.last_name) + ' use command: Izmenenuya PF PGUPS') 
        except (OSError, IOError) as e:
            start_menu(message)
            print('ERROR:', e)
    # При добавлении в главное меню блока добавлять конструкцию IF сюда --->    
    elif message.text == config.markup_2 or message.text == 'Расписание' or message.text == 'расписание':
        rasp_cust_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        rasp_cust_key.add('👷‍ Путевое хоз.', '👨‍💻 Комп.сети') 
        rasp_cust_key.add('🚝 Электроснабж.', '🚃 Орг.перевоз.')
        rasp_cust_key.add('🚂 Тех.эксп.п.с', '🚇 Авт. и телемех.')
        rasp_cust_key.add('Назад')
        msg = bot.send_message(message.chat.id, 'Выбери направление в меню:', reply_markup=rasp_cust_key)
        bot.register_next_step_handler(msg, process_step_kurs)
        
    elif message.text == 'Мне похуй' or message.text == 'Мне Похуй' or message.text == 'мне похуй' or message.text == 'мне Похуй' or message.text == 'мнепохуй':
        msg = bot.send_message(message.chat.id, 'Мне тоже')
        bot.register_next_step_handler(msg, roma)
        print('User: ' + str(message.chat.id) + '@' + str(message.from_user.first_name) + str(message.from_user.last_name) + ' use command: MNE POXYU')
    elif message.text == 'Изменения ППК' or message.text == 'изменения ППК' or message.text == 'изменения ппк' or message.text == 'ИзмененияППК' or message.text == 'измененияппк':
        # Изменения ППК
        try:
            changes_im = Image.open(config.chngPPK_file)
            (width, height) = changes_im.size
            frame = changes_im.crop((0, 385, 603, height - 218))
            frame.save(config.chngPPK_frame)
            photo = open(config.chngPPK_frame, 'rb')
            bot.send_photo(message.chat.id, photo)
            start_menu(message)
            print('User: ' + str(message.chat.id) + '@' + str(message.from_user.first_name) + str(message.from_user.last_name) + ' use command: Izmenenuya PPK')
        except (OSError, IOError) as e:
            start_menu(message)
            print('ERROR:', e)
    elif message.text == 'Расписание 114' or message.text == 'расписание 114' or message.text == 'расписание114' or message.text == 'Расписание114':
        # Расписание 114 группа
        rasp_114 = open(config.rasp_114, 'rb')
        bot.send_photo(message.chat.id, rasp_114)
        start_menu(message)
        print('User: ' + str(message.chat.id) + '@' + str(message.from_user.first_name) + str(message.from_user.last_name) + ' use command: Raspisanie 114')
    elif message.text == 'Бот, налей пивка' or message.text == 'бот, налей пивка' or message.text == 'Бот, налей пива' or message.text == 'бот, налей пива':
        beer = open('beer.jpg', 'rb')
        bot.send_photo(message.chat.id, beer)
        start_menu(message)
        print('User: ' + str(message.chat.id) + '@' + str(message.from_user.first_name) + str(message.from_user.last_name) + ' use command: Beer')
    elif message.text == 'Создать':
        try:
            code = urllib.request.urlopen(config.updatescript_url).getcode()
            print("{0} - {1}".format(config.updatescript_url, code))
            codePPK = urllib.request.urlopen(config.updatescriptPPK_url).getcode()
            print("{0} - {1}".format(config.updatescriptPPK_url, codePPK))
            if (code not in [200, 301]) or (codePPK not in [200, 301]):
                print('ERROR: {0} - {1}')
            else:
                print('UpdateScript: is in progress..')
                print('UpdateScriptPPK: is in progress..')
                driver = webdriver.PhantomJS()
                driver.set_window_size(800, 600)
                driver.get(config.updatescript_url) # url changes
                driver.save_screenshot(config.chng_file)
                driverPPK = webdriver.PhantomJS()
                driverPPK.set_window_size(800, 600)
                driverPPK.get(config.updatescriptPPK_url) # url changes
                driverPPK.save_screenshot(config.chngPPK_file)
                start_menu(message)
                print('UpdateScript: success!')
                print('UpdateScriptPPK: success!')
        except socket.error as e:
            start_menu(message)
            print('Ping Error: ', e)
      
def roma(message):
    if message.text == 'Базаришь?':
        bot.send_message(message.chat.id, 'Конечно')
        start_menu(message)
    else:
        start_menu(message)
def process_step_kurs(message):
    if message.text == '👷‍ Путевое хоз.':
        global chat_id
        global us_first
        global us_last 
        chat_id = message.chat.id
        us_first = message.from_user.first_name
        us_last = message.from_user.last_name
        kb_rasp = types.InlineKeyboardMarkup()
        kb_rasp.add(types.InlineKeyboardButton('П-471', callback_data='П-471'), types.InlineKeyboardButton('П-472', callback_data='П-472'))
        kb_rasp.add(types.InlineKeyboardButton('П-469', callback_data='П-469'), types.InlineKeyboardButton('П-470', callback_data='П-470'))
        kb_rasp.add(types.InlineKeyboardButton('П-468', callback_data='П-468'))
        msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)
        start_menu(message)
        pass
    elif message.text == '👨‍💻 Комп.сети':
        chat_id = message.chat.id
        kb_rasp = types.InlineKeyboardMarkup()
        kb_rasp.add(types.InlineKeyboardButton('ВТ-518', callback_data='ВТ-518'), types.InlineKeyboardButton('ВТ-519,520', callback_data='ВТ-519,520'))
        kb_rasp.add(types.InlineKeyboardButton('ВТ-516', callback_data='ВТ-516'), types.InlineKeyboardButton('ВТ-517', callback_data='ВТ-517'))
        kb_rasp.add(types.InlineKeyboardButton('ВТ-514,515', callback_data='ВТ-514,515'))
        msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)
        start_menu(message)
        pass
    elif message.text == '🚝 Электроснабж.':
        chat_id = message.chat.id
        kb_rasp = types.InlineKeyboardMarkup()
        kb_rasp.add(types.InlineKeyboardButton('Э-289,291', callback_data='Э-289,291'), types.InlineKeyboardButton('Э-285,287', callback_data='Э-285,287'))
        kb_rasp.add(types.InlineKeyboardButton('Э-281,283', callback_data='Э-281,283'), types.InlineKeyboardButton('Э-279', callback_data='Э-279'))
        msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)
        start_menu(message)
        pass
    elif message.text == '🚃 Орг.перевоз.':
        chat_id = message.chat.id
        kb_rasp = types.InlineKeyboardMarkup()
        kb_rasp.add(types.InlineKeyboardButton('Д-370,371', callback_data='Д-370,371'), types.InlineKeyboardButton('Д-372,373', callback_data='Д-372,373'))
        kb_rasp.add(types.InlineKeyboardButton('Д-366,367', callback_data='Д-366,367'), types.InlineKeyboardButton('Д-368,369', callback_data='Д-368,369'))
        kb_rasp.add(types.InlineKeyboardButton('Д-364,365', callback_data='Д-364,365'))
        msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)
        start_menu(message)
        pass
    elif message.text == '🚂 Тех.эксп.п.с':
        chat_id = message.chat.id
        kb_rasp = types.InlineKeyboardMarkup()
        kb_rasp.add(types.InlineKeyboardButton('Т-182', callback_data='Т-182'), types.InlineKeyboardButton('Т-184', callback_data='Т-184'))
        kb_rasp.add(types.InlineKeyboardButton('Т-178,180', callback_data='Т-178,180'), types.InlineKeyboardButton('В-183,185', callback_data='В-183,185'))
        kb_rasp.add(types.InlineKeyboardButton('В-179,181', callback_data='В-179,181'), types.InlineKeyboardButton('В-177', callback_data='В-177'))
        msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)
        start_menu(message)
        pass
    elif message.text == '🚇 Авт. и телемех.':
        chat_id = message.chat.id
        kb_rasp = types.InlineKeyboardMarkup()
        kb_rasp.add(types.InlineKeyboardButton('Ш-288,290', callback_data='Ш-288,290'), types.InlineKeyboardButton('Ш-280,282', callback_data='1'))
        kb_rasp.add(types.InlineKeyboardButton('Ш-284,286', callback_data='Ш-284,286'))
        msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)
        start_menu(message)
        pass
    elif message.text == 'Назад':
        start_menu(message)
        pass

@bot.callback_query_handler(func=lambda data_rasp: True)
def inline(data_rasp):
    if data_rasp.data == 'П-471':
        photo_rasp = open('p-471.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'П-472':
        photo_rasp = open('p-472.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'П-469':
        photo_rasp = open('p-469.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'П-470':
        photo_rasp = open('p-470.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'П-468':
        photo_rasp = open('p-468.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'ВТ-518':
        photo_rasp = open('vt-518.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'ВТ-519,520':
        photo_rasp = open('vt-519.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'ВТ-516':
        photo_rasp = open('vt-516.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'ВТ-517':
        photo_rasp = open('vt-517.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'ВТ-514,515':
        photo_rasp = open('vt-514.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Э-289,291':
        photo_rasp = open('e-289.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Э-285,287':
        photo_rasp = open('e-285.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Э-281,283':
        photo_rasp = open('e-281.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Э-279':
        photo_rasp = open('e-279.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Д-370,371':
        photo_rasp = open('d-370.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Д-372,373':
        photo_rasp = open('d-372.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Д-366,367':
        photo_rasp = open('d-366.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Д-368,369':
        photo_rasp = open('d-368.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Д-364,365':
        photo_rasp = open('d-364.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Т-182':
        photo_rasp = open('t-182.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Т-184':
        photo_rasp = open('t-184.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Т-178,180':
        photo_rasp = open('t-178.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'В-183,185':
        photo_rasp = open('v-183.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'В-179,181':
        photo_rasp = open('v-179.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'В-177':
        photo_rasp = open('v-177.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS') 
        pass
    elif data_rasp.data == 'Ш-288,290':
        photo_rasp = open('sh-288.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Ш-280,282':
        photo_rasp = open('sh-280.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    elif data_rasp.data == 'Ш-284,286':
        photo_rasp = open('sh-284.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        print('User: ' + str(chat_id) + '@' + str(us_first) + str(us_last) + ' use command: Raspisanie PF PGUPS')
        pass
    
if __name__ == '__main__':
     bot.polling(none_stop=True)


