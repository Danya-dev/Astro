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
    
  
def runge_kutta(coor, vel, planets):
    G = 6.67408E-11    
    x = coor[0]
    y = coor[1]
    vx = vel[0]
    vy = vel[1]
    ax = 0
    ay = 0
        
    for planet in planets: 
        distance = math.sqrt((x - planet.real_coord[0])**2 + 
                         (y - planet.real_coord[1])**2)
        cos = (x - planet.real_coord[0]) / distance
        sin = (y - planet.real_coord[1]) / distance
        acceleration = G * planet.mass / distance**2
        ax -= G * planet.mass / distance**2 * cos
        ay -= G * planet.mass / distance**2 * sin
            
    k1 = [vx, vy, ax, ay]
        
    x2 = x + 0.5 * dt * vx
    y2 = y + 0.5 * dt * vy
    vx2 = vx + 0.5 * dt * ax
    vy2 = vy + 0.5 * dt * ay
    
    for planet in planets: 
        distance = math.sqrt((x2 - planet.real_coord[0])**2 + 
                         (y2 - planet.real_coord[1])**2)
        cos = (x2 - planet.real_coord[0]) / distance
        sin = (y2 - planet.real_coord[1]) / distance
        acceleration = G * planet.mass / distance**2
        ax2 = 0 - G * planet.mass / distance**2 * cos
        ay2 = 0 - G * planet.mass / distance**2 * sin
            
    k2 = [vx2, vy2, ax2, ay2]
        
    x3 = x + 0.5 * dt * vx2
    y3 = y + 0.5 * dt * vy2
    vx3 = vx + 0.5 * dt * ax2
    vy3 = vy + 0.5 * dt * ay2
        
    for planet in planets: 
        distance = math.sqrt((x3 - planet.real_coord[0])**2 + 
                         (y3 - planet.real_coord[1])**2)
        cos = (x3 - planet.real_coord[0]) / distance
        sin = (y3 - planet.real_coord[1]) / distance
        acceleration = G * planet.mass / distance**2
        ax3 = 0 - G * planet.mass / distance**2 * cos
        ay3 = 0 - G * planet.mass / distance**2 * sin
            
    k3 = [vx3, vy3, ax3, ay3]
        
    x4 = x + dt * vx3
    y4 = y + dt * vy3
    vx4 = vx + dt * ax3
    vy4 = vy + dt * ay3
        
    for planet in planets: 
        distance = math.sqrt((x4 - planet.real_coord[0])**2 + 
                         (y4 - planet.real_coord[1])**2)
        cos = (x4 - planet.real_coord[0]) / distance
        sin = (y4 - planet.real_coord[1]) / distance
        acceleration = G * planet.mass / distance**2
        ax4 = 0 - G * planet.mass / distance**2 * cos
        ay4 = 0 - G * planet.mass / distance**2 * sin
            
    k4 = [vx4, vy4, ax4, ay4]

    coor[0] += (k1[0] + 2*k2[0] + 2*k3[0] + k4[0])*dt / 6
    coor[1] += (k1[1] + 2*k2[1] + 2*k3[1] + k4[1])*dt / 6
    vel[0] += (k1[2] + 2*k2[2] + 2*k3[2] + k4[2])*dt / 6
    vel[1] += (k1[3] + 2*k2[3] + 2*k3[3] + k4[3])*dt / 6
    return coor, vel

def rotation(surface):
    return pg.transform.rotate(surface, 1)

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
          
          
class Rocket(pg.sprite.Sprite): #класс ракета
    def __init__(self, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.w , self.h = self.image.get_size()
        self.coord = [100, 300]  # Координаты на экране в пикселах.
        self.real_coord = [100*scale_param, 300*scale_param]  # Координаты в пространстве. 
        self.rect = self.image.get_rect(center=(self.coord[0], self.coord[1]))
        self.mask = pg.mask.from_surface(self.image)
        self.angle = 0
        self.velocity = [0,0]
        
    def motion(self): #функция движения
        self.findangle(self.velocity)
        self.coord[0] = int(self.real_coord[0] / scale_param)
        self.coord[1] = int(self.real_coord[1] / scale_param)
        self.rect = self.image.get_rect(center=(self.coord[0], self.coord[1]))
        
    def findangle(self, direction):
        if direction[0] > 0:
           self.angle = math.degrees(math.atan2(-direction[1], direction[0]) )
        if direction[0] < 0:
           self.angle = math.degrees(math.atan2(-direction[1], direction[0]) - math.pi)   
           
    def draw(self, surf, image, topleft, angle):
            rotated_image = pg.transform.rotate(image, angle)
            new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

            surf.blit(rotated_image, new_rect.topleft)
            pg.draw.rect(surf, (255, 0, 0), new_rect, 2)
    def gravity(self, planets): 
        """ гравитация. принимаем на вход массив планет """
        z = runge_kutta(self.real_coord, self.velocity, planets)
        self.real_coord = z[0]
        self.velocity = z[1]
    
    def trajectory(self, planets):
        """ траектория по которой будет двигаться ракета, если двигатели не будут работать"""
        G = 6.67408E-11
        v0 = self.velocity[0]
        v1 = self.velocity[1]
        c0 = self.real_coord[0]
        c1 = self.real_coord[1]
        A = []
        for i in range(200):
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
    
class Dust(pg.Rect):
    def draw(self):
        pg.draw.rect(screen, (0,255,0), self)
        
class Asteroid(pg.sprite.Sprite):
    def __init__(self, filename, x, y, rad, mass):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.coord = [x,y]  # Координаты на экране в пикселах.
        self.real_coord = [x*scale_param, y*scale_param]  # Координаты в пространстве.  
        self.rad = rad
        self.mass = mass        
        self.rect = self.image.get_rect(center=(self.coord[0], self.coord[1]))
        self.mask = pg.mask.from_surface(self.image)
    
        
        
class Finish(pg.sprite.Sprite):
    def __init__(self, filename, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.coord = [x,y]  # Координаты на экране в пикселах.       
        self.rect = self.image.get_rect(center=(self.coord[0], self.coord[1]))
        self.mask = pg.mask.from_surface(self.image)
    
class Level(): 
    pass


class Level_1(Level):
    def __init__(self,clock, events):
        gamegoes = True
        while gamegoes:
            self.preparation()
            self.start(clock, events)
            gamegoes = self.process(clock, events)
        menu.menufunc(clock, events)
            
            
            
    def preparation(self):
        self.rocket = Rocket("Rocket.png")
        self.planets = []
        self.dustclouds = []
        self.asteroids = []
        self.objfinish = Finish("Earth.png",500, 300)
        self.planets.append(Planet(400, 300, 40, 8E+28))
        self.width = 30
        self.asteroids.append(Asteroid("Asteroid.png", 200, 200, 40, 10))
        self.dustclouds.append(Dust(0, 0,SCREEN_SIZE[0] , self.width))
        self.dustclouds.append(Dust(0,0, self.width, SCREEN_SIZE[1]))
        self.dustclouds.append(Dust(0,SCREEN_SIZE[1] - self.width,SCREEN_SIZE[0], self.width ))
        #self.dustclouds.append(Dust(SCREEN_SIZE[0] - self.width,0, self.width, SCREEN_SIZE[1]))
                
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
                    self.rocket.findangle(rocdirect)   
                elif launchbool and event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1 :
                        
                        pg.draw.circle(screen,(233,100,8),(100,100),50 )
                        mod = math.sqrt(rocdirect[0]**2 + rocdirect[1]**2)                       
                        self.rocket.velocity = [round(math.exp(force) * rocdirect[0] / mod),
                                                round(math.exp(force) * rocdirect[1] / mod)]
                        return None
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
            if self.oncollision():
                return True
            if self.finish():
                return False
            
            pg.display.flip()
        
    def drawthemall(self):
        self.rocket.trajectory(self.planets)
        
        for planet in self.planets:
            planet.draw()
        for dust in self.dustclouds :
            dust.draw()
        for asteroid in self.asteroids :
            screen.blit(asteroid.image, asteroid.rect)  
        corner_cords = [self.rocket.coord[0] - self.rocket.w/2,
                        self.rocket.coord[1] - self.rocket.h/2]
        self.rocket.draw(screen, self.rocket.image, corner_cords, self.rocket.angle)

        
        screen.blit(self.objfinish.image, self.objfinish.rect)
        
        
    def movethemall(self):
        self.rocket.motion()      
        
    def oncollision(self):
        for dust in self.dustclouds:
            if dust.collidepoint(self.rocket.coord[0], self.rocket.coord[1]):
                return True
        for asteroid in self.asteroids:
            r1 = int(self.rocket.coord[0] - self.rocket.image.get_width()/2)
            r2 = int(self.rocket.coord[1] - self.rocket.image.get_height()/2)
            a1 = int(asteroid.coord[0] - asteroid.image.get_width()/2)
            a2 = int(asteroid.coord[1] - asteroid.image.get_height()/2)
            offset = (r1 - a1, r2 - a2)
            if asteroid.mask.overlap_area(self.rocket.mask, offset) > 0:
                return True
            
    def finish(self):
        r1 = int(self.rocket.coord[0] - self.rocket.image.get_width()/2)
        r2 = int(self.rocket.coord[1] - self.rocket.image.get_height()/2)
        a1 = int(self.objfinish.coord[0] - self.objfinish.image.get_width()/2)
        a2 = int(self.objfinish.coord[1] - self.objfinish.image.get_height()/2)
        offset = (r1 - a1, r2 - a2)
        if self.objfinish.mask.overlap_area(self.rocket.mask, offset) > 0:
            return True
                                    
    
    
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Astro")

clock = pg.time.Clock()
menu = Menu(screen)    

menu.menufunc(clock, pg.event)

pg.quit()

