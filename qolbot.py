# libraries
import sys
import os
import time
import telepot
import json
from telepot.loop import MessageLoop
from wakeonlan import send_magic_packet
from random import random
from random import seed
from pprint import pprint

# mocking spongebob ( https://github.com/dhildebr/spongebob-case )
def to_spongecase(orig, cap_chance = 0.5):
  orig = str(orig)
  if len(orig) <= 1:
    return (orig.upper() if (random() < cap_chance) else orig.lower())
  else:
    seed(orig)
    
    spongecase = []
    for ch in orig:
      case_choice = random() < cap_chance
      spongecase.append(ch.upper() if (case_choice) else ch.lower())
    
    return ''.join(spongecase)

# validate chat_id
def IsValidChatID(id):
   try:
      cfg['chat_ids'].index(id)
      return True
   except:
      return False

# validate permission
def IsPublic(cmd):
   true_cmd = cmd.split(' ', 1)[0]
   try:
      cfg['public_cmds'].index(true_cmd)
      return True
   except:
      if cmd[0] != '/':
         return True
      return False

# check if 'cmd' can be used by 'chat_id'
def CanAnswer(cmd, chat_id):
   if IsPublic(cmd):
      return True
   elif IsValidChatID(chat_id):
      return True
   return False

# run commands
def Execute(cmd):
   true_cmd = cmd.split(' ', 1)[0]
   if true_cmd == '/wol':
      send_magic_packet(cfg['wol_mac'])
      return 'Sent WoL to ' + cfg['wol_mac']
   elif true_cmd == '/shutdown':
      os.system('sudo shutdown -h now')
      return 'Bot Offline'
   elif true_cmd == '/spongemock':
      txt = cmd.replace('/spongemock','')
      try:
         return to_spongecase(txt)
      except:
         return 'fatal_error: StiaMO ENtRAndo daVVERo nel RIDiCOLO'
   else:
      try:
         return to_spongecase(cmd)
      except:
         return 'fatal_error: StiaMO ENtRAndo daVVERo nel RIDiCOLO'


# message handling
def HandleTgMsg(msg):
   content_type, chat_type, chat_id = telepot.glance(msg)
    
   #debug info
   if cfg['debug']:
      print(content_type, chat_type, chat_id)

   #check if user has permission and eventually answer
   if (content_type == 'text'):
      if CanAnswer(msg['text'], chat_id):
         bot.sendMessage(chat_id, Execute(msg['text']))


## SETUP

CONFIG_PATH = 'config.json'

# Get configuration info
if len(sys.argv) > 1:
   CONFIG_PATH = sys.argv[1]

with open(CONFIG_PATH) as json_file:
   cfg = json.load(json_file)

# Create Bot and send notice of being online
bot = telepot.Bot(cfg['bot_token'])

for id in cfg['chat_ids']:
   bot.sendMessage(id, 'Bot Online')

# Check if there are old messages and completely ignore them
updates = bot.getUpdates()

if(len(updates) != 0):
   off = updates[len(updates)-1]['update_id']
   MessageLoop(bot, HandleTgMsg).run_as_thread(offset = off + 1)
else:
   MessageLoop(bot, HandleTgMsg).run_as_thread()

# Loop
while 1:
   time.sleep(10)
