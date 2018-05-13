import time
import os
import periphery
import telepot
from telepot.loop import MessageLoop

class TelepotBot:
    TOKEN = '<Insert Token Here>'

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(msg)
        print('content_type: {0}, chat_type: {1}, chat_id: {2}'.format(content_type, chat_type, chat_id))
        print(telepot.flavor(msg))

        if content_type != 'text':
            return

        _from = msg['from']
        command = msg['text']
        print_msg = 'Got command: {0} from {1} {2}'.format(command, _from['first_name'], _from['last_name'])
        print(print_msg)
        if chat_id != 480607298:
            self.bot.sendMessage(480607298, print_msg)

        if command == '/picture':
            self.periphery.takePicture('new.jpg')
            picture = open('/home/pi/chiliBot/new.jpg', 'rb')
            self.bot.sendPhoto(chat_id, picture)
        elif command == '/light_on':
            self.periphery.setLightState(True)
            self.bot.sendMessage(chat_id, 'Erldedigt! Licht ist an!')
        elif command == '/light_off':
            self.periphery.setLightState(False)
            self.bot.sendMessage(chat_id, 'Erledigt! Licht ist aus!')
        elif command == '/heat_on':
            self.periphery.setHeatState(True)
            self.bot.sendMessage(chat_id, 'Erldedigt! Heitmatte ist an!')
        elif command == '/heat_off':
            self.periphery.setHeatState(False)
            self.bot.sendMessage(chat_id, 'Erledigt! Heizmatte ist aus!')
        elif command == '/data':
            self.periphery.fetchNewDHTValues()
            licht = 'x' if self.periphery.light else '_'
            heizmatte = 'x' if self.periphery.heat else '_'
            humidity, temperature = self.periphery.readLastDHTValues()
            self.bot.sendMessage(chat_id, ('Temperatur: {0:0.1f}°C,\n' + 
                                    'Luftfeuchtigkeit: {1:0.1f}%,\n'+
                                    '[{2}] Licht\n[{3}] Heizmatte').format(temperature,
                                                                                humidity,
                                                                                licht,
                                                                                heizmatte))

    def __init__(self, periphery):
        self.bot = telepot.Bot(self.TOKEN)
        self.periphery = periphery
        MessageLoop(self.bot, self.handle).run_as_thread()

    

