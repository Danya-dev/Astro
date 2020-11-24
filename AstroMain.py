import pygame as pg
import botton
import math

pg.init()
pg.font.init()

SCREEN_SIZE = (800, 600)
FPS_menu = 15
FPS = 100
dt = FPS*5E+2
scale_param = 5E+8
"""Масштабирование экранных координат по отношению к физическим.
Тип: float
Мера: количество пикселей на один метр."""
    
  
class Menu():
        '''Класс меню. Реализует отрисовку меню и функции меню.'''
        def __init__(self, screen):
            self.screen = screen
            self.levels = botton.Botton(self.screen, [100, 50], 120, 40,
                                        (255, 0, 0), "Уровни")
            self.settings = botton.Botton(self.screen, [100, 100], 120, 40,
                                          (255, 0, 0), "Настройки")
            self.info = botton.Botton(self.screen, [100, 150], 120, 40,
                                      (255, 0, 0), "Об игре")
            self.back = botton.Botton(self.screen, [100, 500], 120, 40,
                                      (255, 0, 0), "Назад")
            self.position = 1  
            # Позиция меню. 1 - главное, 2 - уровни, 3 - настройки,
            # 4 - об игре, 5 - переход к уровню
            self.level_1 = botton.Botton(self.screen, [100, 50], 120, 40,
                                         (255, 0, 0), "Уровень 1")
        
        def menufunc(self, clock, events): # Функция меню. 
            done = False
            while not done: # Обработка событий.
                clock.tick(FPS_menu)
    
                for event in events.get():
                    if event.type == pg.QUIT:
                        done = True 
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.position == 1:  
                            if self.levels.click(event.pos):
                                self.position = 2
                            elif self.settings.click(event.pos):
                                self.position = 3
                            elif self.info.click(event.pos):
                                self.position = 4
                        elif  self.position == 2:   
                            if self.back.click(event.pos):
                                self.position = 1
                            elif self.level_1.click(event.pos):
                                return Level_1(clock, events)
                        else:   
                            if self.back.click(event.pos):
                                self.position = 1   
            
                pg.display.flip()
                self.draw()
        
        def draw(self):
            screen.fill((0, 0, 0))
            if self.position == 1:
                self.levels.draw()
                self.settings.draw()
                self.info.draw()
            if self.position == 2:
                self.level_1.draw()
                self.back.draw()
            if self.position == 3:
                self.back.draw()
            if self.position == 4:
                self.back.draw()
    
        def levels(self):
            pass
        
        def setting(self):
            pass
        
        def info(self):
            pass            
          
          
class Rocket(): #класс ракета
    def __init__(self):

        self.coord = [100, 300]  # Координаты на экране в пикселах.
        self.real_coord = [100*scale_param, 300*scale_param]  # Координаты в пространстве. 


        self.velocity = [0,0]
        
    def motion(self): #функция движения
        self.real_coord[0] += self.velocity[0] * dt
        self.real_coord[1] += self.velocity[1] * dt
        self.coord[0] = int(self.real_coord[0] / scale_param)
        self.coord[1] = int(self.real_coord[1] / scale_param)
    
        
    def draw(self): #рисуем ракету каждый clock.tick
        pg.draw.circle(screen, (255,255,255),
                     self.coord, 20)
    def gravity(self, planets): 
        """ гравитация. принимаем на вход массив планет """
        G = 6.67408E-11
        for planet in planets: 


            distance = math.sqrt((self.real_coord[0] - planet.real_coord[0])**2 + 
                                 (self.real_coord[1] - planet.real_coord[1])**2)
            cos = (self.real_coord[0] - planet.real_coord[0]) / distance

            acceleration = G * planet.mass / distance**2
            sin = (self.real_coord[1] - planet.real_coord[1]) / distance
            self.velocity[0] -= acceleration * cos * dt
            self.velocity[1] -= acceleration * sin * dt 
    
    def trajectory(self, planets):
        """ траектория по которой будет двигаться ракета, если двигатели не будут работать"""
        G = 6.67408E-11
        v0 = self.velocity[0]
        v1 = self.velocity[1]
        c0 = self.real_coord[0]
        c1 = self.real_coord[1]
        A = []
        for i in range(50):
            for planet in planets: 

                distance = math.sqrt((c0 - planet.real_coord[0])**2 + 
                                  (c1 - planet.real_coord[1])**2)
                cos = (c0 - planet.real_coord[0]) / distance

                acceleration = G * planet.mass / distance**2
                sin = (c1 - planet.real_coord[1]) / distance
                v0 -= acceleration * cos * dt
                v1 -= acceleration * sin * dt 
                A.append((int(c0/scale_param), int(c1/scale_param)))
                c0 += v0 * dt
                c1 += v1 * dt
                
        pg.draw.aalines(screen, (0, 255, 0), False, A, 5)

        
class Planet(): 
    def __init__(self, x, y, rad, mass):
        self.coord = [x,y]  # Координаты на экране в пикселах.
        self.real_coord = [x*scale_param, y*scale_param]  # Координаты в пространстве.  
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

        self.planets.append(Planet(400, 300, 40, 2E+30))


        
        
        
        
        if self.start(clock, events) :
            self.process(clock, events)
     #функция обрабатывает запуск ракеты  
    def start(self, clock, events):            
        done = False
        launchbool = False

        force = 6

        rocdirect = [1,0]
        while not done: #обработка событий
            clock.tick(30 )
            screen.fill((0,0,0))            
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.MOUSEBUTTONDOWN :
                    if event.button == 1:                
                        launchbool = True    
                elif launchbool and event.type == pg.MOUSEMOTION:
                    rocdirect = [self.rocket.coord[0] - event.pos[0],
                                 self.rocket.coord[1] - event.pos[1] ]
                        
                elif launchbool and event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1 :
                        
                        pg.draw.circle(screen,(233,100,8),(100,100),50 )
                        mod = math.sqrt(rocdirect[0]**2 + rocdirect[1]**2)                       
                        self.rocket.velocity = [round(math.exp(force) * rocdirect[0] / mod),
                                                round(math.exp(force) * rocdirect[1] / mod)]
                        return True
                if launchbool :
                    force += 0.2 
                        
            self.drawthemall()
            pg.display.flip()
        
          
    def process(self, clock, events):
        #функция обрабатывает полет ракеты    
        done = False
        while not done: #обработка событий

            clock.tick(FPS)

            screen.fill((0,0,0))
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
            self.rocket.gravity(self.planets)
            self.movethemall()
            self.drawthemall()
            
            pg.display.flip()
        
    def drawthemall(self):
        self.rocket.trajectory(self.planets)
        
        for planet in self.planets:
            planet.draw()
    

        self.rocket.draw()
        
        
    def movethemall(self):
        self.rocket.motion()
    
    
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Astro")

clock = pg.time.Clock()
menu = Menu(screen)    

level = menu.menufunc(clock, pg.event)

pg.quit()

