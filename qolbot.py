# libraries
import sys
import os
import time
import telepot
import json
import unidecode
from telepot.loop import MessageLoop
from wakeonlan    import send_magic_packet
from gpiozero     import CPUTemperature
from random       import random
from random       import seed
from pprint       import pprint

# mocking spongebob ( https://github.com/dhildebr/spongebob-case )
def to_spongecase(orig, cap_chance = 0.2):
   orig = unidecode.unidecode(orig)

   if len(orig) <= 1:
      return (orig.upper() if (random() < cap_chance) else orig.lower())
   else:
      spongecase = []
      for ch in orig:
         case_choice = random() < cap_chance
         spongecase.append(ch.upper() if (case_choice) else ch.lower())
         cap_chance = 1 - cap_chance
    
      return ''.join(spongecase)

# CPU temp
def GetCPUTemp():
   tmp = CPUTemperature()
   return str(tmp.temperature) + ' *C' 

# validate chat_id
def IsValidChatID(id):
   try:
      cfg['chat_ids'].index(id)
      return True
   except:
      return False

# validate permission
def IsPublic(cmd):
   try:
      cfg['public_cmds'].index(cmd)
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

# message handling
def HandleTgMsg(msg):
   content_type, chat_type, chat_id = telepot.glance(msg)
    
   #debug info
   if cfg['debug']:
      print(content_type, chat_type, chat_id)

   if (content_type == 'text'):
      # split incoming text in the format
      # /command[@botname] [argument]
      rx_command = msg['text']
      tmp = rx_command.split(' ', 1)   #split '/command@botname' from 'argument'
      command = tmp[0].split('@', 1)[0]
      if (rx_command[0] != '/'):
         argument = rx_command
      elif (len(tmp) == 1):
         argument = '' 
      else:
         argument = tmp[1]

      #check if user has permission and eventually answer
      if CanAnswer(command, chat_id):
         # bot.sendMessage(chat_id, Execute(command, argument))
         if command == '/wol':
            # wake on lan
            send_magic_packet(cfg['wol_mac'])
            bot.sendMessage (chat_id, 'Sent WoL to ' + cfg['wol_mac'])
         elif command == '/shutdown':
            # shut down rpi
            bot.sendMessage (chat_id, 'Bot Offline')
            os.system('sudo shutdown -h now')
         elif command == '/cputemp':
            bot.sendMessage(chat_id, 'CPU temperature is ' + GetCPUTemp())
         elif (command == '/spongemock' or command[0] != '/'):
            # spongemock response
            if (len(argument) > 0):
               try:
                  bot.sendMessage (chat_id, to_spongecase(argument))
               except:
                  bot.sendMessage (chat_id, 'fatal_error: StiaMO ENtRAndo daVVERo nel RIDiCOLO')
         else:
            return 'Unknown command'


## SETUP

CONFIG_PATH = 'config.json'

# Get configuration info
if len(sys.argv) > 1:
   CONFIG_PATH = sys.argv[1]

with open(CONFIG_PATH) as json_file:
   cfg = json.load(json_file)

# Create Bot and send notice of being online
bot = telepot.Bot(cfg['bot_token'])

for id in cfg['chat_ids_service']:
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
