#!/usr/bin/python

#import
import display

class Menu:
    def __init__(self, display):
        self.currentSelection = -1
        self.topItem = 0
        self.completeMenu = []
        self.display = display

    def setMenu(self, menu):
        self.completeMenu = menu

    def displayMenu(self)
        if self.currentSelection == -1:
            return
        line1 = self.completeMenu[topItem]
        line2 = self.completeMenu[topItem+1]
        line3 = self.completeMenu[topItem+2]
        line4 = self.completeMenu[topItem+3]
        self.display.setDisplay()

    def nextMenu(self):
        pass

    def prevMenu(self):
        pass

    def selectMenu(self):
        pass