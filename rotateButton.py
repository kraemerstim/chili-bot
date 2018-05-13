# coding=utf-8
# Benoetigte Module werden importiert und eingerichtet
import RPi.GPIO as GPIO
from Util.Observer import Observable
import time

class RotateButton:
    PIN_CLK = 24
    PIN_DT = 23
    BUTTON_PIN = 18

    def buttonRotate(self):
        self.PIN_CLK_AKTUELL = GPIO.input(RotateButton.PIN_CLK)

        if self.PIN_CLK_AKTUELL != self.PIN_CLK_LETZTER:
    
            if GPIO.input(RotateButton.PIN_DT) != self.PIN_CLK_AKTUELL:
                Richtung = True # Uhrzeigersinn
            else:
                Richtung = False # gegen Uhrzeigersinn
    
        self.PIN_CLK_LETZTER = self.PIN_CLK_AKTUELL
    
    def buttonPressed(self):
        pass

    def __init__(self):
        self.PIN_CLK_LETZTER = 0
        self.IN_CLK_AKTUELL = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RotateButton.PIN_CLK, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(RotateButton.PIN_DT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(RotateButton.BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        self.PIN_CLK_LETZTER = GPIO.input(RotateButton.PIN_CLK)
        GPIO.add_event_detect(RotateButton.PIN_CLK, GPIO.BOTH, callback=self.buttonRotate, bouncetime=50)
        GPIO.add_event_detect(RotateButton.BUTTON_PIN, GPIO.FALLING, callback=self.buttonPressed, bouncetime=50)
        self.rotate_notifier = RotateButton.RotateNotifier(self)
        self.button_press_notifier = RotateButton.ButtonPressNotifier(self)

    class RotateNotifier(Observable):
        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self, clockwise):
            Observable.notifyObservers(self, clockwise)

    class ButtonPressNotifier(Observable):
        def __init__(self, outer):
            Observable.__init__(self)
            self.outer = outer

        def notifyObservers(self):
            Observable.notifyObservers(self)