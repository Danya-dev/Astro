# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 13:55:48 2020

@author: Филипп
"""

Class Botton():
    '''Класс кнопки.'''
    def __init__(self, screen, coord, height, width, color, text):
        self.screen = screen
        self.coord = coord
        self.height = height
        self.width = width
        self.color = color
        self.text = text
        
    def draw(self):
        pass
    
    def click(self):
        pass