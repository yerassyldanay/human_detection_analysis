import telebot
import redis
import json
import traceback
import constants as C
from time import sleep

# bot = telebot.TeleBot('964340126:AAGrtPar34wCCtDnEsrvDIfFv8ZXCUa_O7w', False)
bot = telebot.TeleBot(C.telegram_api, False)

def is_int(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

def is_mine(camera_id):
	if camera_id != None and not is_int(camera_id):
		return False
	try:
		redis_cli = redis.StrictRedis(host = C.redis_host, port = C.redis_port, db = 0)
		objects = redis_cli.get(camera_id + '_last')
	except:
		return False
	if objects != None:
		return True
	return False

def merge(objects, old_objects):
	objects = json.loads(objects.decode('utf-8'))
	old_objects = json.loads(old_objects.decode('utf-8'))
	for obj in old_objects:
		objects.append(obj)
	return json.dumps(objects)

def except_it(camera_id, ttl):
	print(ttl)
	try:
		redis_cli = redis.StrictRedis(host = C.redis_host, port = C.redis_port, db = 0)
		objects = redis_cli.get(camera_id + '_last')
		if objects != None:
			old_objects = redis_cli.get(camera_id + '_none')
			if old_objects != None:
				objects = merge(objects, old_objects)

			redis_cli.setex(camera_id + '_none', ttl * 60, objects)
			return True
	except Exception:
		print('Error:\n', traceback.format_exc())
	return False

@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text[0:2] == 'ex' or message.text[0:2] == 'Ex':
		arr = message.text.split()
		camera_id = -1
		if len(arr) == 2:
			camera_id = arr[1]
		if camera_id != -1 and is_mine(camera_id):
			markup = telebot.types.InlineKeyboardMarkup(row_width=5)
			button1 = telebot.types.InlineKeyboardButton(text='10m', callback_data='_1_'+camera_id)
			button2 = telebot.types.InlineKeyboardButton(text='30m', callback_data='_2_'+camera_id)
			button3 = telebot.types.InlineKeyboardButton(text='1h', callback_data='_3_'+camera_id)
			button4 = telebot.types.InlineKeyboardButton(text='6h', callback_data='_4_'+camera_id)
			button5 = telebot.types.InlineKeyboardButton(text='9h', callback_data='_5_'+camera_id)
			markup.add(button1, button2)
			markup.add(button3, button4, button5)
			bot.send_message(reply_to_message_id=message.message_id,chat_id=message.chat.id, text='ID: ' + camera_id + ', choose time', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	if call.data != '-1':
		if call.data[0] == '_':
			times = [10, 30, 60, 360, 540]
			ttl = times[int(call.data[1]) - 1]
			camera_id = call.data[3:]
			if except_it(camera_id, ttl):
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Excepted for " + str(ttl) + " minute")
	else:
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ok")

@bot.message_handler(commands=['except', 'ex'])
def text_arrived(message):
    arr = message.text.split()
    camera_id = -1
    if len(arr) == 2:
        camera_id = arr[1]
    if camera_id != -1 and is_mine(camera_id):
        markup = telebot.types.InlineKeyboardMarkup(row_width=5)
        button1 = telebot.types.InlineKeyboardButton(text='10m', callback_data='_1_'+camera_id)
        button2 = telebot.types.InlineKeyboardButton(text='30m', callback_data='_2_'+camera_id)
        button3 = telebot.types.InlineKeyboardButton(text='1h', callback_data='_3_'+camera_id)
        button4 = telebot.types.InlineKeyboardButton(text='6h', callback_data='_4_'+camera_id)
        button5 = telebot.types.InlineKeyboardButton(text='9h', callback_data='_5_'+camera_id)
        markup.add(button1, button2)
        markup.add(button3, button4, button5)
        bot.send_message(reply_to_message_id=message.message_id,chat_id=message.chat.id, text='ID: ' + camera_id + ', choose time', reply_markup=markup)

bot.polling()
