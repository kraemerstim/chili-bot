#!/usr/bin/env python3

import time
import os
import Util.configReader as configReader
import periphery
import displayController
import telepotBot

class chiliIO:
    def __init__(self):
        self.periphery = periphery.Periphery()
        self.display = displayController.DisplayController(self.periphery)
        self.bot = telepotBot.TelepotBot(self.periphery)
        configReader.initialize()

    def getFilePath(self, aFilePath):
        return os.path.join(os.path.dirname(__file__), aFilePath)
        
    def cleanup(self):
        self.display.cleanup()
    
    #Display
    def resetDisplay(self):
        self.display.resetDisplay()

    #ConfigReader  
    def getIniValue(self, aSection, aKey):
        return configReader.getIniValue(aSection, aKey)
