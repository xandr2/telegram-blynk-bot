Python + telegram bot + blynk = love)

I like Blynk and also I like telegram. I wrote a telegram bot in python which helps me managing my IoT projects at home. You can managing different progects in one menu. Watch a demo:

 [![demo](http://img.youtube.com/vi/zdYiJ7SiDgo/0.jpg)](https://www.youtube.com/watch?v=zdYiJ7SiDgo "telegram bot and blynk")

### Python
  - Install libs:
```bash
pip install python-telegram-bot
pip install blynkapi
```
  - Copy template python code from [GitHub](https://github.com/xandr2/telegram-blynk-bot/blob/master/blynkbot.py)

### Create telegram bot
  - First of all you need [install telegram](https://telegram.org/) to your device
  - Talk to [BotFather](@botfather) for [creating your own bot](https://core.telegram.org/bots)
  - Copy your bot id to python program `blynkbot.py` as var `tokenid`

### Blynk
  - Create project [link](http://docs.blynk.cc/#getting-started)
  - Add hardware [link](http://docs.blynk.cc/#getting-started-getting-started-with-hardware-how-to-use-an-example-sketch)
  - Get [auth token](http://docs.blynk.cc/#getting-started-getting-started-with-hardware-auth-token) and copy it to python program `blynkbot.py` as var `my_project`
  - Create or modify objects in `blynkbot.py` (k_amp_power, k_amp_src, k_light)
  - Run your bot `./blynkbot.py`

### Details
  - [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
  - [blynkapi](https://github.com/xandr2/blynkapi)

### Issue
  - Can't talk to bot via Google voice. [issue](http://android.stackexchange.com/questions/155928/send-message-to-telegram-bot-via-google-now-voice-command)

