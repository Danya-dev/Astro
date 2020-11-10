import pygame as pg
import math
pg.init()
pg.font.init()

SCREEN_SIZE = (800, 600)

class button():
    pass
    
class Menu(): 

        
    def menufunc(self, clock, events): # функция меню 
        done = False
        while not done: #обработка событий
            clock.tick(15)
    
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True 
                    """ нажимаем кнопку чтобы начать"""
                elif event.type == pg.KEYDOWN: 
                    return Level_1(clock, events)
                """теперь обрабатывать события будет функция start класса level"""
                
                
            pg.display.flip()
class Rocket(): #класс ракета
    def __init__(self):
        self.coord = [50, 400]
        self.velocity = [0,0]
        
    def motion(self): #функция движения
        self.coord[0] += self.velocity[0]
        self.coord[1] += self.velocity[1]
    
        
    def draw(self): #рисуем рокету каждый clock.tick
        pg.draw.circle(screen, (255,255,255),
                     self.coord, 20)
    def gravity(self, planets): 
        """ гравитация. принимаем на вход массив планет """
        g = 0.1
        for planet in planets: 

            distance = math.sqrt((self.coord[0] - planet.coord[0])**2 + 
                                 (self.coord[1] - planet.coord[1])**2)
            cos = (self.coord[0] - planet.coord[0]) / distance
            acceleration = g * planet.mass / distance**2
            sin = (self.coord[1] - planet.coord[1]) / distance
            self.velocity[0] -= int(acceleration * cos)
            self.velocity[1] -= int(acceleration * sin)    
    
        
class Planet(): 
    def __init__(self, x, y, rad, mass):
        self.coord = [x,y]
        self.rad = rad
        self.mass = mass
    def draw(self):
        pg.draw.circle(screen, (255,0,50),
                       self.coord, self.rad)
    
    
class Level(): 
    pass

class Level_1(Level):
    def __init__(self,clock, events):
        self.rocket = Rocket()
        self.planets = []
        self.planets.append(Planet(400, 300, 80, 1000000))
        
        
        
        self.start(clock,events)
     #функция обрабатывает запуск ракеты  
    def start(self, clock, events):            
        done = False
        while not done: #обработка событий
            clock.tick(15)
            screen.fill((0,0,0))
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.KEYDOWN:
                    self.rocket.velocity = [3,-6]
                    #теперь обрабатывать события будет функция process
                    self.process(clock, events)
            self.drawthemall()
            pg.display.flip()
            
    def process(self, clock, events):
        #функция обрабатывает полет ракеты    
        done = False
        while not done: #обработка событий
            clock.tick(30)
            screen.fill((0,0,0))
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
            self.rocket.gravity(self.planets)
            self.movethemall()
            self.drawthemall()
                
                
            pg.display.flip()
        
    def drawthemall(self):
        self.rocket.draw()
        
        for planet in self.planets:
            planet.draw()
        
        
    def movethemall(self):
        self.rocket.motion()
    
    
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Astro")

clock = pg.time.Clock()

"""создаем объект меню """
menu = Menu()     

""" функция выкидывает нам тип уровня:"""
level = menu.menufunc(clock, pg.event)




pg.quit()

