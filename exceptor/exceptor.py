import telebot
import redis
import json
from time import sleep

redis_cli = redis.StrictRedis(host = "local_redis", port = 6379, db = 0)
bot = telebot.TeleBot('964340126:AAGrtPar34wCCtDnEsrvDIfFv8ZXCUa_O7w', False)
# keyboard1 = telebot.types.ReplyKeyboardMarkup()
# keyboard1.row('Привет', 'Пока')

def merge(objects, old_objects):
    objects = json.loads(objects.decode('utf-8'))
    old_objects = json.loads(old_objects.decode('utf-8'))
    for obj in old_objects:
        objects.append(obj)
    return json.dumps(objects)

def except_it(camera_id, ttl):
    objects = redis_cli.get(camera_id + '_last')
    if objects != None:
        old_objects = redis_cli.get(camera_id + '_none')
        if old_objects != None:
            objects = merge(objects, old_objects)

        redis_cli.setex(camera_id + '_none', ttl * 60, objects)
        print(ttl)
        return True
    return False

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.find(bot.get_me().username) != -1:
        arr = message.text.split()
        ttl = 0
        if len(arr) == 2:
            ttl = 30
        if len(arr) == 3:
            ttl = int(arr[2])
        if len(arr) == 4:
            ttl = int(arr[2]) * 60 + int(arr[3])
        if ttl != 0 and except_it(arr[1], ttl):
            bot.send_message(message.chat.id, "Done")
                # bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMzXjv4n1veCPdd2sgQruKikY5udwcAAucCAAK6wJUFFgQ7qkIwU1QYBA')
            # else:
            #     bot.send_message(message.chat.id, "Done")
            

    # if message.text.lower() == 'привет':
    #     bot.send_message(message.chat.id, 'Привет, мой создатель')
    # elif message.text.lower() == 'пока':
    #     bot.send_message(message.chat.id, 'Прощай, создатель')
    # elif message.text.lower() == 'asd':
    #     bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMzXjv4n1veCPdd2sgQruKikY5udwcAAucCAAK6wJUFFgQ7qkIwU1QYBA')

bot.polling()

# while True: # Don't let the main Thread end.
#     pass