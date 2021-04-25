import telebot
import datetime
import os

from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
def replace(file_path):
    #Create temp file
    fh, abs_path = mkstemp()
    some_list = ["[SHOPIFY]","[FASTLY]","[TUMBLR]"]
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:

                list6 = []
                list6.append(line)
                durum =[x for x in some_list if any(x in item for item in list6)]
                if len(durum)==0:
                    new_file.write(line)
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
replace("/home/ubuntu/results.txt")

def tele( ):
    now =datetime.datetime.now().strftime("%m/%d/%Y, %H:%M")
    token = "YOUR-BOT-TOKEn"
    bot = telebot.TeleBot(token)
    #message = "{} \n {}".format(title, url)
    file= open("/home/ubuntu/results.txt","rb")
    bot.send_document(chat_id="YOUR-CHAT-ID", caption=now,data=file)

if os.stat("/home/ubuntu/results.txt").st_size > 0:
    tele()
