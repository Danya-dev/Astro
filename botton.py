# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 13:55:48 2020

@author: Филипп
"""
import pygame as pg

pg.init()

class Botton():
    '''Класс кнопки.'''
    def __init__(self, screen, coords, width, height, color, text):
        self.screen = screen
        self.coords = coords
        self.height = height
        self.width = width
        self.color = color
        self.text = text
        self.font = pg.font.SysFont("dejavusansmono", 25)
        
    def draw(self):
        ltop_corner = (self.coords[0] - int(self.width / 2), 
                       self.coords[1] - int(self.height / 2))
        pg.draw.rect(self.screen, self.color, (ltop_corner[0], ltop_corner[1],
                    self.width, self.height))
        botton_text = self.font.render(self.text, True, (255, 255, 255))
        self.screen.blit(botton_text, (ltop_corner[0], self.coords[1]))
        
    
    def click(self, mouse_coord):
        if (mouse_coord[0] >= self.coords[0] - self.width / 2) & (
            mouse_coord[0] <= self.coords[0] + self.width / 2) & (
            mouse_coord[1] >= self.coords[1] - self.height / 2) & (
            mouse_coord[1] <= self.coords[1] + self.height / 2):
                    return True
        else:
            return False
    
