#!/usr/bin/python

#import
import time
import threading
from threading import Thread
from Util.Observer import Observer
import lcd

class DisplayController:
    LCD_WIDTH = 20

    def __init__(self, periphery):
        self.lcd_lock = threading.Lock()
        self.display_number = 0
        self.line1 = "Chili-Bot"
        self.line2 = ""
        self.line3 = ""
        self.line4 = "by Tim Kraemer"
        self.periphery = periphery
        self.dhtObserver= DisplayController.DHTObserver(self)
        self.externalObserver= DisplayController.ExternalObserver(self)
        self.periphery.dht_changed.addObserver(self.dhtObserver)
        self.periphery.external_changed.addObserver(self.externalObserver)
        lcd.lcd_init()


    def __get_line_part(self, line, iteration):
        scount = len(line)
        if scount <= self.LCD_WIDTH:
            return line

        step = iteration % (scount-self.LCD_WIDTH+10)
        start = step - 5 #start berechnen
        if (start <= 0):
            start = 0
        
        if start > (scount - self.LCD_WIDTH):
            start = (scount - self.LCD_WIDTH)
        
        return line[start:(start + self.LCD_WIDTH)]
        
    def resetDisplay(self):
        self.display_number += 1
        line1 = 'Licht: '
        if (self.periphery.light):
            line1 += 'on'
        else:
            line1 += 'off'

        line2 = 'Heizmatte: '
        if (self.periphery.light):
            line2 += 'on'
        else:
            line2 += 'off'

        line3 = 'Temperatur: {0:0.1f}°C, '.format(self.periphery.temperature)
        line4 = 'Temperatur: {0:0.1f}%, '.format(self.periphery.humidity)
        if len(line1) <= self.LCD_WIDTH and len(line2) <= self.LCD_WIDTH:
            self.__secure_set_display(line1, line2, line3, line4, 2)
        else:
            Thread(target=self.__threaded_display_move, args=(self.display_number, line1, line2, line3, line4)).start()
        print(line1)
        print(line2)
        print(line3)
        print(line4)

    def __secure_set_display(self, line1, line2, line3, line4, style=2):
        self.lcd_lock.acquire()
        try:
            lcd.lcd_display(line1, line2, line3, line4, style)
        finally:
            self.lcd_lock.release()
    
    def __threaded_display_move(self, displaynumber, line1, line2, line3, line4, interval=0.2):
        iteration = 0
        while (self.display_number == displaynumber):
            _line1 = self.__get_line_part(line1, iteration)
            _line2 = self.__get_line_part(line2, iteration)
            _line3 = self.__get_line_part(line3, iteration)
            _line4 = self.__get_line_part(line4, iteration)
            self.__secure_set_display(_line1, _line2, _line3, _line4)
            iteration += 1
            time.sleep(interval)
    
    def cleanup(self):
        self.__secure_set_display('Bye bye', ':(', ':(', ':(')
        lcd.GPIO.cleanup()
    
    class DHTObserver(Observer):
        def __init__(self, outer):
            self.outer = outer

        def update(self, observable, arg):
            self.outer.resetDisplay()

    class ExternalObserver(Observer):
        def __init__(self, outer):
            self.outer = outer
            
        def update(self, observable, arg):
            self.outer.resetDisplay()


    
