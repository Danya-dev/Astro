# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 13:44:05 2020

@author: Филипп
"""
import pygame as pg
import Botton

pg.init()

class Menu():
    '''Класс меню. Реализует отрисовку меню и функции меню.'''
    def __init__(self, screen):
        self.screen = screen
        self.levels = Botton(self.screen, 100, 50, 60, 40, (255, 0, 0), "Levels")
        self.settings = Botton(self.screen, 100, 100, 60, 40, (255, 0, 0), "Settings")
        self.info = Botton(self.screen, 100, 150, 60, 40, (255, 0, 0), "Information")
        
    def draw(self):
        screen.fill((0, 0, 0))
        self.levels.draw()
        self.setting.draw()
        self.info.draw()
    
    def levels(self):
        pass
    
    def setting(self):
        pass
    
    def info(self):
        pass