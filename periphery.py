import os
from Util.Observer import Observable
import Adafruit_DHT
import time

DHT_DATA_PIN = 4
DHT_SENSOR = Adafruit_DHT.DHT22

class Periphery:
    def __init__(self):
        self.dht_changed = DHTChangedNotifier(self)
        self.external_changed = ExternalChangedNotifier(self)
        self.fetchNewDHTValues()
        self.heat = False
        self.light = False
        self.setHeatState(False)
        self.setLightState(False)

    def readLastDHTValues(self):
        return(self.humidity, self.temperature)

    def fetchNewDHTValues(self):
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_DATA_PIN)
        if humidity is not None and temperature is not None:
            self.humidity, self.temperature = (humidity, temperature)
            self.dht_changed.notifyObservers()
        else:
            self.humidity = 0
            self.temperature = 0

    def setLightState(self, lighton):
        enable = '1' if lighton else '0'
        for i in range(10):
            os.system('/home/pi/chiliBot/send 10001 1 ' + enable)
            time.sleep(0.1)
            
        if self.light != lighton:
            self.light = lighton
            self.external_changed.notifyObservers()

    def setHeatState(self, heaton):
        enable = '1' if heaton else '0'
        for i in range(10):
            os.system('/home/pi/chiliBot/send 10001 2 ' + enable)
            time.sleep(0.1)
        
        if self.heat != heaton:
            self.heat = heaton
            self.external_changed.notifyObservers()
    
    def takePicture(self, filename='picture.jpg'):
        os.system('/home/pi/chiliBot/takePicture.sh ' + filename)

class DHTChangedNotifier(Observable):
    def __init__(self, outer):
        Observable.__init__(self)
        self.outer = outer

    def notifyObservers(self):
        Observable.notifyObservers(self, {'humidity': self.outer.humidity, 'temperature': self.outer.temperature})

class ExternalChangedNotifier(Observable):
    def __init__(self, outer):
        Observable.__init__(self)
        self.outer = outer

    def notifyObservers(self):
        self.setChanged()
        Observable.notifyObservers(self, {'light': self.outer.light, 'heat': self.outer.heat})