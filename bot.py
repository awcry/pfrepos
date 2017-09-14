#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config              # main config with token
import telebot
from telebot import types  # inline types
import cherrypy
import urllib
import socket
import time
import logging
from selenium import webdriver
from PIL import Image

bot = telebot.TeleBot(config.token)

WEBHOOK_HOST = 'www.pfpgupsbot.herokuapp.com'
WEBHOOK_PORT = 8443  # 443, 80, 88 ��� 8443 (���� ������ ���� ������!)
WEBHOOK_LISTEN = 'www.pfpgupsbot.herokuapp.com'  # �� ��������� �������� �������� ��������� ����� �� IP, ��� � ����

WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # ���� � �����������
WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # ���� � ���������� �����

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)
            
@bot.message_handler(commands=['start'])
def start_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('👁 Меню') 
    username = message.from_user.first_name
    msg = bot.send_message(message.chat.id, 'Выберите Меню', reply_markup=markup) # Текст приветствия

@bot.message_handler(func=lambda message: message.text == '👁 Меню')
def menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(config.markup_1) 
    markup.add(config.markup_2)
    username = message.from_user.first_name
    msg = bot.send_message(message.chat.id, 'Чем я могу Вам помочь, ' + username + '?', reply_markup=markup)
    
@bot.message_handler(func=lambda message: message.text == 'Создать')
def create(message):
    try:
        code = urllib.request.urlopen(config.updatescript_url).getcode()
        print("{0} - {1}".format(config.updatescript_url, code))
        codePPK = urllib.request.urlopen(config.updatescriptPPK_url).getcode()
        print("{0} - {1}".format(config.updatescriptPPK_url, codePPK))
        if (code not in [200, 301]) or (codePPK not in [200, 301]):
            print('ERROR: {0} - {1}')
        else:
            print('UPDATESCRIPT: is in progress..')
            print('UPDATESCRIPTPPK: is in progress..')
            driver = webdriver.PhantomJS()
            driver.set_window_size(800, 600)
            driver.get(config.updatescript_url) # url changes
            driver.save_screenshot(config.chng_file)
            driverPPK = webdriver.PhantomJS()
            driverPPK.set_window_size(800, 600)
            driverPPK.get(config.updatescriptPPK_url) # url changes
            driverPPK.save_screenshot(config.chngPPK_file)
            print('UPDATESCRIPT: success!')
            print('UPDATESCRIPTPPK: success!')
    except socket.error as e:
        print('PING ERROR: ', e)
       
@bot.message_handler(func=lambda message: message.text == config.markup_1) 
def changes(message):
    chat_id = message.chat.id
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
        print('USER: ' + str(message.chat.id) + '@' + str(message.from_user.first_name) + str(message.from_user.last_name) + ' used command: CHANGES PF PGUPS') 
    except (OSError, IOError) as e:
        print('ERROR:', e)
        
@bot.message_handler(func=lambda message: message.text == config.markup_2)  
def rasp(message):
    rasp_cust_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    rasp_cust_key.add('👷‍ Путевое хоз.', '👨‍💻 Комп.сети') 
    rasp_cust_key.add('🚝 Электроснабж.', '🚃 Орг.перевоз.')
    rasp_cust_key.add('🚂 Тех.эксп.п.с', '🚇 Авт. и телемех.')
    rasp_cust_key.add('👁 Меню')
    msg = bot.send_message(message.chat.id, 'Выбери направление в меню:', reply_markup=rasp_cust_key)
    print('USER: ' + str(message.chat.id) + '@' + str(message.from_user.first_name) + str(message.from_user.last_name) + ' used command: RASPISANIE PF PGUPS')
    
@bot.message_handler(func=lambda message: message.text == '👷‍ Путевое хоз.') 
def put(message):
    global chat_id
    #global us_first
    #global us_last 
    chat_id = message.chat.id
    #us_first = message.from_user.first_name
    #us_last = message.from_user.last_name
    kb_rasp = types.InlineKeyboardMarkup()
    kb_rasp.add(types.InlineKeyboardButton('П-471', callback_data='П-471'), types.InlineKeyboardButton('П-472', callback_data='П-472'))
    kb_rasp.add(types.InlineKeyboardButton('П-469', callback_data='П-469'), types.InlineKeyboardButton('П-470', callback_data='П-470'))
    kb_rasp.add(types.InlineKeyboardButton('П-468', callback_data='П-468'))
    msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)

@bot.message_handler(func=lambda message: message.text == '👨‍💻 Комп.сети') 
def vte(message):
    global chat_id
    chat_id = message.chat.id
    kb_rasp = types.InlineKeyboardMarkup()
    kb_rasp.add(types.InlineKeyboardButton('ВТ-518', callback_data='ВТ-518'), types.InlineKeyboardButton('ВТ-519,520', callback_data='ВТ-519,520'))
    kb_rasp.add(types.InlineKeyboardButton('ВТ-516', callback_data='ВТ-516'), types.InlineKeyboardButton('ВТ-517', callback_data='ВТ-517'))
    kb_rasp.add(types.InlineKeyboardButton('ВТ-514,515', callback_data='ВТ-514,515'))
    msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)

@bot.message_handler(func=lambda message: message.text == '🚝 Электроснабж.') 
def electro(message):
    global chat_id
    chat_id = message.chat.id
    kb_rasp = types.InlineKeyboardMarkup()
    kb_rasp.add(types.InlineKeyboardButton('Э-289,291', callback_data='Э-289,291'), types.InlineKeyboardButton('Э-285,287', callback_data='Э-285,287'))
    kb_rasp.add(types.InlineKeyboardButton('Э-281,283', callback_data='Э-281,283'), types.InlineKeyboardButton('Э-279', callback_data='Э-279'))
    msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)

@bot.message_handler(func=lambda message: message.text == '🚃 Орг.перевоз.') 
def dvij(message):
    global chat_id
    chat_id = message.chat.id
    kb_rasp = types.InlineKeyboardMarkup()
    kb_rasp.add(types.InlineKeyboardButton('Д-370,371', callback_data='Д-370,371'), types.InlineKeyboardButton('Д-372,373', callback_data='Д-372,373'))
    kb_rasp.add(types.InlineKeyboardButton('Д-366,367', callback_data='Д-366,367'), types.InlineKeyboardButton('Д-368,369', callback_data='Д-368,369'))
    kb_rasp.add(types.InlineKeyboardButton('Д-364,365', callback_data='Д-364,365'))
    msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)

@bot.message_handler(func=lambda message: message.text == '🚂 Тех.эксп.п.с') 
def teh(message):
    global chat_id
    chat_id = message.chat.id
    kb_rasp = types.InlineKeyboardMarkup()
    kb_rasp.add(types.InlineKeyboardButton('Т-182', callback_data='Т-182'), types.InlineKeyboardButton('Т-184', callback_data='Т-184'))
    kb_rasp.add(types.InlineKeyboardButton('Т-178,180', callback_data='Т-178,180'), types.InlineKeyboardButton('В-183,185', callback_data='В-183,185'))
    kb_rasp.add(types.InlineKeyboardButton('В-179,181', callback_data='В-179,181'), types.InlineKeyboardButton('В-177', callback_data='В-177'))
    msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)

@bot.message_handler(func=lambda message: message.text == '🚇 Авт. и телемех.') 
def automat(message):
    global chat_id
    chat_id = message.chat.id
    kb_rasp = types.InlineKeyboardMarkup()
    kb_rasp.add(types.InlineKeyboardButton('Ш-288,290', callback_data='Ш-288,290'), types.InlineKeyboardButton('Ш-280,282', callback_data='1'))
    kb_rasp.add(types.InlineKeyboardButton('Ш-284,286', callback_data='Ш-284,286'))
    msg = bot.send_message(message.chat.id, 'Выбери группу и нажми на нее:', reply_markup=kb_rasp)    
    
@bot.callback_query_handler(func=lambda data_rasp: True)
def inline(data_rasp):
    if data_rasp.data == 'П-471':
        photo_rasp = open('p-471.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
    elif data_rasp.data == 'П-472':
        photo_rasp = open('p-472.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        pass
    elif data_rasp.data == 'П-469':
        photo_rasp = open('p-469.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        pass
    elif data_rasp.data == 'П-470':
        photo_rasp = open('p-470.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        pass
    elif data_rasp.data == 'П-468':
        photo_rasp = open('p-468.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        pass
    elif data_rasp.data == 'ВТ-518':
        photo_rasp = open('vt-518.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)      
        pass
    elif data_rasp.data == 'ВТ-519,520':
        photo_rasp = open('vt-519.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)        
        pass
    elif data_rasp.data == 'ВТ-516':
        photo_rasp = open('vt-516.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)        
        pass
    elif data_rasp.data == 'ВТ-517':
        photo_rasp = open('vt-517.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)       
        pass
    elif data_rasp.data == 'ВТ-514,515':
        photo_rasp = open('vt-514.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)        
        pass
    elif data_rasp.data == 'Э-289,291':
        photo_rasp = open('e-289.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)        
        pass
    elif data_rasp.data == 'Э-285,287':
        photo_rasp = open('e-285.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)      
        pass
    elif data_rasp.data == 'Э-281,283':
        photo_rasp = open('e-281.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)       
        pass
    elif data_rasp.data == 'Э-279':
        photo_rasp = open('e-279.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)       
        pass
    elif data_rasp.data == 'Д-370,371':
        photo_rasp = open('d-370.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)       
        pass
    elif data_rasp.data == 'Д-372,373':
        photo_rasp = open('d-372.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)        
        pass
    elif data_rasp.data == 'Д-366,367':
        photo_rasp = open('d-366.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)      
        pass
    elif data_rasp.data == 'Д-368,369':
        photo_rasp = open('d-368.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)       
        pass
    elif data_rasp.data == 'Д-364,365':
        photo_rasp = open('d-364.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)     
        pass
    elif data_rasp.data == 'Т-182':
        photo_rasp = open('t-182.png', 'rb')
        bot.send_photo(chat_id, photo_rasp) 
        pass
    elif data_rasp.data == 'Т-184':
        photo_rasp = open('t-184.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)        
        pass
    elif data_rasp.data == 'Т-178,180':
        photo_rasp = open('t-178.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        pass
    elif data_rasp.data == 'В-183,185':
        photo_rasp = open('v-183.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)       
        pass
    elif data_rasp.data == 'В-179,181':
        photo_rasp = open('v-179.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        pass
    elif data_rasp.data == 'В-177':
        photo_rasp = open('v-177.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        pass
    elif data_rasp.data == 'Ш-288,290':
        photo_rasp = open('sh-288.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)        
        pass
    elif data_rasp.data == 'Ш-280,282':
        photo_rasp = open('sh-280.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)     
        pass
    elif data_rasp.data == 'Ш-284,286':
        photo_rasp = open('sh-284.png', 'rb')
        bot.send_photo(chat_id, photo_rasp)
        pass

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Disable CherryPy requests log
access_log = cherrypy.log.access_log
for handler in tuple(access_log.handlers):
    access_log.removeHandler(handler)

# Start cherrypy server
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})            
    


