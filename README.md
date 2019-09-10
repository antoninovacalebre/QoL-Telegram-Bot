# QoL-Telegram-Bot
This Telegram Bot gives various quality of life services. They can be set to be available only to certain chat_ids,or to be public.

## Installation Instructions
Install `telepot`
```
sudo pip install telepot
```
and `wakeonlan`
```
sudo pip install wakeonlan
```
Then get the files from the repo
```
git clone https://github.com/atvacs/WoL-Telegram-Bot.git
```
Then move to the created directory and access the `config.json` file
```
cd WoL-Telegram-Bot
```
```
sudo nano config.json
```
Inside `config.json` add your settings, then save and exit. You can then start the application with
```
sudo python wolbot.py &
```
If you want the script to run at system startup, access `/etc/rc.local`
```
sudo nano /etc/rc.local
```
and add this line at the end of the file, but before `exit 0`
```
sudo python /full/path/to/wolbot.py /full/path/to/config.json & 
```
The `&` is necessary since we use an infinite loop.

## Important
* The `chat_ids` specified in `config.json` can request the private services
* Add commands to the `public_cmds` array to set which one are publicly available (mocking spongebob is always public)
* telepot library is needed (install via pip)
* wakeonlan library is needed (install via pip)
