import pygame as pg
import botton
import math

pg.init()
pg.font.init()

SCREEN_SIZE = (800, 600)
FPS_menu = 15
FPS = 400
dt = 100*5E+2
scale_param = 5E+8
"""Масштабирование экранных координат по отношению к физическим.
Тип: float
Мера: количество пикселей на один метр."""
RIGHT = "turn to the right"
LEFT = "turn to the left"
UP = "speed up"
DOWN = "speed down"
STOP = "not turn"

canvas = pg.Surface(SCREEN_SIZE)
window = pg.display.set_mode((SCREEN_SIZE))
space = pg.image.load("space5.png").convert_alpha()
screenpos = (0, 0)
    
  
def runge_kutta(coor, vel, planets):
    """
    Функция, реализующая расчёт движения в гравитационном поле с помощью
    метода Рунге-Кутты.

    Parameters
    ----------
    coor : list
        Координаты тела.
    vel : list
        Скорость тела.
    planets : list
        Список планет.

    Returns
    -------
    coor : list
        Новые координаты тела.
    vel : list
        Новая скорость тела.

    """
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
            self.levels = botton.Botton_image(self.screen, [90 , 513],
                                              "play.png", "circle")
            self.settings = botton.Botton_image(self.screen, [184 , 540],
                                                "settings.png", "circle")
            self.back = botton.Botton(self.screen, [100, 100], 120, 40,
                                      (0, 0, 0), "Назад")
            self.position = 1  
            # Позиция меню. 1 - главное, 2 - уровни, 3 - настройки,
            # 4 - переход к уровню
            self.level_1 = botton.Botton_image(self.screen, [61, 487],
                                                "level_1.png", "rect")
            self.level_2 = botton.Botton_image(self.screen, [117 , 495],
                                                "level_2.png", "rect")
            self.level_3 = botton.Botton_image(self.screen, [173 , 496],
                                                "level_3.png", "rect")
            self.sett = botton.Botton(self.screen, [160, 150], 240, 40,
                                         (0, 0, 0), "Всё уже настроено!")
        
        
        def menufunc(self, clock, events): # Функция меню. 
            done = False
            while not done: # Обработка событий.
                clock.tick(FPS_menu)
                for event in events.get():
                    if event.type == pg.QUIT:
                        done = True 
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if self.position == 1:  
                            if self.levels.click(event.pos):
                                self.position = 2
                            elif self.settings.click(event.pos):
                                self.position = 3
                        elif self.position == 2:   
                            if self.back.click(event.pos):
                                self.position = 1
                            elif self.level_1.click(event.pos):
                                return Level_1(clock, events)
                            elif self.level_2.click(event.pos):
                                return Level_2(clock, events)
                            elif self.level_3.click(event.pos):
                                return Level_3(clock, events)
                        else:   
                            if self.back.click(event.pos):
                                self.position = 1   
            
                pg.display.flip()
                self.draw()
        
        
        def draw(self):
            screen.blit(space, screenpos)
            if self.position == 1:
                self.levels.draw()
                self.settings.draw()
            if self.position == 2:
                self.level_1.draw()
                self.level_2.draw()
                self.level_3.draw()
                self.back.draw()
            if self.position == 3:
                self.sett.draw()
                self.back.draw()
    
        
        def levels(self):
            pass
            
           
        def setting(self):
            pass
            
            
        def info(self):
            pass
          
          
class Rocket(pg.sprite.Sprite):
    """Класс ракеты."""
    def __init__(self, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.w , self.h = self.image.get_size()
        self.coord0 = [100, 300]
        self.coord = [100, 300] # Координаты на экране в пикселах.
        self.real_coord = [100*scale_param, 300*scale_param]  # Координаты в пространстве. 
        self.rect = self.image.get_rect(center=(self.coord[0], self.coord[1]))
        self.mask = pg.mask.from_surface(self.image)
        self.angle = 0
        self.velocity = [0,0]
        self.cam = [0, 0]
        
    
    def motion(self):
        """Функция движения ракеты."""
        self.findangle(self.velocity)
        self.coord[0] = int(self.real_coord[0] / scale_param)
        self.coord[1] = int(self.real_coord[1] / scale_param)
        self.rect = self.image.get_rect(center=(self.coord[0], self.coord[1]))
        
    
    def findangle(self, direction):
        if direction[0] > 0:
           self.angle = math.degrees(math.atan2(-direction[1], direction[0]) )
        if direction[0] < 0:
           self.angle = math.degrees(-math.atan2(-direction[1], -direction[0]) - math.pi)   
           
   
    def draw(self, surf, image, topleft, angle):
            rotated_image = pg.transform.rotate(image, angle)
            new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
            surf.blit(rotated_image, new_rect.topleft)
            # pg.draw.rect(surf, (255, 0, 0), new_rect, 2)
            
    
    def gravity(self, planets): 
        """ гравитация. принимаем на вход массив планет """
        z = runge_kutta(self.real_coord, self.velocity, planets)
        self.real_coord = z[0]
        self.velocity = z[1]


    def trajectory(self, planets, n):
        """Траектория по которой будет двигаться ракета,
        если двигатели не будут работать."""
        [c0, c1] = self.real_coord
        [v0, v1] = self.velocity
        A = []
        done = False
        i = 0
        while i < n and not done:
            A.append((int(c0/scale_param) - self.coord[0] + self.coord0[0],
                      int(c1/scale_param) - self.coord[1] + self.coord0[1]))
            z = runge_kutta([c0, c1], [v0, v1], planets)
            [c0, c1] = z[0]
            [v0, v1] = z[1]
            for planet in planets:     
                r1 = int((int(c0/scale_param)) - self.image.get_width()/2)
                r2 = int((int(c1/scale_param)) - self.image.get_height()/2)
                a1 = int(planet.coord[0] - planet.image.get_width()/2)
                a2 = int(planet.coord[1] - planet.image.get_height()/2)
                offset = (r1 - a1, r2 - a2)
                if planet.mask.overlap_area(self.mask, offset) > 0 and i > 0:
                    done = True
            i += 1
        pg.draw.aalines(screen, (200, 0, 150), False, A, 5)
        
   
    def activate(self, motion, dv):
        if motion == LEFT:
            self.velocity[0] -= dv * math.sin(math.radians(self.angle))
            self.velocity[1] -= dv * math.cos(math.radians(self.angle))
        elif motion == RIGHT:
            self.velocity[0] += dv * math.sin(math.radians(self.angle))
            self.velocity[1] += dv * math.cos(math.radians(self.angle))
        elif motion == UP:
            self.velocity[0] += dv * math.cos(math.radians(self.angle))
            self.velocity[1] -= dv * math.sin(math.radians(self.angle))
        elif motion == DOWN:
            if self.velocity[0]**2 + self.velocity[1]**2 <= 10000:
                pass
            else:
                self.velocity[0] -= dv * math.cos(math.radians(self.angle))
                self.velocity[1] += dv * math.sin(math.radians(self.angle))
        elif motion == STOP:
            pass

        
class Planet(pg.sprite.Sprite): 
    def __init__(self, filename, x, y, rad, mass):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.coord = [x,y]  # Координаты на экране в пикселах.
        self.real_coord = [x*scale_param, y*scale_param]  # Координаты в пространстве.  
        self.rad = rad
        self.mass = mass
        self.mask = pg.mask.from_surface(self.image)
    
    
    def draw(self, x, y):
        self.rect = self.image.get_rect(center=(x + self.coord[0], y + self.coord[1]))
        screen.blit(self.image, self.rect)
    
    
class Dust():
    def __init__(self, x, y, w, h):
        self.rec0 = pg.Rect(x, y, w, h)
        self.a = x
        self.b = y
        self.c = [w, h]
    
    
    def draw(self, x, y):
        self.rec1 = pg.Rect((x + self.a, y + self.b), self.c)
        pg.draw.rect(screen, (0,255,0), self.rec1)
        
        
class Asteroid(pg.sprite.Sprite):
    
    def __init__(self, filename, x, y, rad, mass):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.coord = [x,y]  # Координаты на экране в пикселах.
        self.real_coord = [x*scale_param, y*scale_param]  # Координаты в пространстве.  
        self.rad = rad
        self.mass = mass        
        self.mask = pg.mask.from_surface(self.image)
    
    
    def draw(self, x, y):
        self.rect = self.image.get_rect(center=(x + self.coord[0], y + self.coord[1]))
        screen.blit(self.image, self.rect)
        
        
        
class Finish(pg.sprite.Sprite):
    def __init__(self, filename, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.coord = [x,y]  # Координаты на экране в пикселах.       
        self.rect = self.image.get_rect(center=(self.coord[0], self.coord[1]))
        self.mask = pg.mask.from_surface(self.image)
    
    
    def draw(self, x, y):
        self.rect = self.image.get_rect(center=(x + self.coord[0], y + self.coord[1]))
        screen.blit(self.image, self.rect)


class Level():
    def __init__(self, clock, events):
        self.rocket = Rocket("Rocket.png")
        self.planets = []
        self.dustclouds = []
        self.asteroids = []
        self.dv = 20
        self.width = 30
        self.lenth_start_traject = 150
        gamegoes = True
        while gamegoes:
            self.preparation()
            self.start(clock, events)
            gamegoes = self.process(clock, events)
        menu.menufunc(clock, events)       
            
            
    def preparation(self):
        """Функция готовит объекты игрового поля."""
        self.rocket = Rocket("Rocket.png")
        self.planets = []
        self.dustclouds = []
        self.asteroids = []
        self.objfinish = Finish("Earth.png",550, 300)
        self.planets.append(Planet("Planet2.png", 300, 300, 40, 8E+28))
        self.width = 30
                
      
    def start(self, clock, events):
        """Функция обрабатывает запуск ракеты."""
        done = False
        launchbool = False
        force = 50
        rocdirect = [1,0]
        mouse_coord = self.rocket.coord
        trajectory = False
        while not done: # Обработка событий.
            clock.tick(30 )
            screen.blit(space, screenpos)            
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.MOUSEBUTTONDOWN :
                    if event.button == 1:                
                        launchbool = True  
                        trajectory = True
                elif launchbool and event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1 :
                        done = True
                elif launchbool:
                    if event.type == pg.MOUSEMOTION:
                        mouse_coord = event.pos
                    rocdirect = [-self.rocket.coord[0] + mouse_coord[0],
                                 -self.rocket.coord[1] + mouse_coord[1] ]
                    self.rocket.findangle(rocdirect)
                    self.rocket.velocity[0] = force * rocdirect[0]
                    self.rocket.velocity[1] = force * rocdirect[1]                
            
            if trajectory:
                self.rocket.trajectory(self.planets, self.lenth_start_traject)                 
            self.drawthemall()
            pg.display.flip()
        
          
    def process(self, clock, events):
        """Функция обрабатывает полет ракеты."""    
        done = False
        motion = STOP
        while not done: # Обработка событий.
            clock.tick(FPS)
            screen.blit(space, screenpos)
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.KEYDOWN: 
                    if event.key == pg.K_r:
                        Level_1(clock, events)
                        done = True
                        return False
                    elif (event.key == pg.K_SPACE) or (event.key == pg.K_ESCAPE):
                        i = 0
                        while i < 1:
                            done = True
                            for event in events.get():
                                if event.type == pg.QUIT:
                                    i = 1
                                elif event.type == pg.KEYDOWN:
                                    if event.key == pg.K_r:
                                        i = 1
                                        done = False
                                        Level_1(clock, events)
                                    elif(event.key == pg.K_SPACE) or (event.key == pg.K_ESCAPE):
                                        i = 1  
                                        done = False
                    elif event.key == pg.K_LEFT:
                        motion = LEFT
                    elif event.key == pg.K_RIGHT:
                        motion = RIGHT
                    elif event.key == pg.K_UP:
                        motion = UP
                    elif event.key == pg.K_DOWN:
                        motion = DOWN
                elif event.type == pg.KEYUP:
                    if event.key in [pg.K_LEFT,
                                 pg.K_RIGHT]:
                        motion = STOP
         
            self.rocket.activate(motion, self.dv)
            self.rocket.gravity(self.planets)
            self.rocket.trajectory(self.planets, 150)
            self.movethemall()
            self.drawthemall()
            if self.oncollision():
                return True
            if self.finish():
                return False
            pg.display.flip()
       
        
    def drawthemall(self):
        x = - self.rocket.coord[0] + self.rocket.coord0[0] 
        """x прибавляется к координатам изображений
        для создания эффекта движения камеры"""
        y = - self.rocket.coord[1] + self.rocket.coord0[1]
        for planet in self.planets:
            planet.draw(x, y)
        for dust in self.dustclouds :
            dust.draw(x, y)
        for asteroid in self.asteroids :
            asteroid.draw(x, y)
        corner_cords = [self.rocket.coord0[0] - self.rocket.w/2,
                        self.rocket.coord0[1] - self.rocket.h/2]
        self.rocket.draw(screen, self.rocket.image, corner_cords, self.rocket.angle)
        screen.blit(self.objfinish.image, self.objfinish.rect)
        self.objfinish.draw(x, y)
      
        
    def movethemall(self):
        self.rocket.motion()      
        
        
    def oncollision(self):
        for dust in self.dustclouds:
            if dust.rec0.collidepoint(self.rocket.coord[0], self.rocket.coord[1]):
                return True
        for asteroid in self.asteroids:
            r1 = int(self.rocket.coord[0] - self.rocket.image.get_width()/2)
            r2 = int(self.rocket.coord[1] - self.rocket.image.get_height()/2)
            a1 = int(asteroid.coord[0] - asteroid.image.get_width()/2)
            a2 = int(asteroid.coord[1] - asteroid.image.get_height()/2)
            offset = (r1 - a1, r2 - a2)
            if asteroid.mask.overlap_area(self.rocket.mask, offset) > 0:
                return True
        for planet in self.planets:
            r1 = int(self.rocket.coord[0] - self.rocket.image.get_width()/2)
            r2 = int(self.rocket.coord[1] - self.rocket.image.get_height()/2)
            a1 = int(planet.coord[0] - planet.image.get_width()/2)
            a2 = int(planet.coord[1] - planet.image.get_height()/2)
            offset = (r1 - a1, r2 - a2)
            if planet.mask.overlap_area(self.rocket.mask, offset) > 0:
                return True
    
    
    def finish(self):
        r1 = int(self.rocket.coord[0] - self.rocket.image.get_width()/2)
        r2 = int(self.rocket.coord[1] - self.rocket.image.get_height()/2)
        a1 = int(self.objfinish.coord[0] - self.objfinish.image.get_width()/2)
        a2 = int(self.objfinish.coord[1] - self.objfinish.image.get_height()/2)
        offset = (r1 - a1, r2 - a2)
        if self.objfinish.mask.overlap_area(self.rocket.mask, offset) > 0:
            return True
        
class Level_1(Level): 
    def __init__(self, clock, events):
        super().__init__(clock, events)
        
    
    def preparation(self):
        """Функция готовит объекты игрового поля."""
        self.rocket = Rocket("Rocket.png")
        self.planets = []
        self.dustclouds = []
        self.asteroids = []
        self.objfinish = Finish("Earth.png",550, 300)
        self.planets.append(Planet("Planet2.png", 300, 300, 40, 8E+28))
        self.asteroids.append(Asteroid("Asteroid1.png", 100, 200, 40, 10))
        
class Level_2(Level): 
    def __init__(self, clock, events):
        super().__init__(clock, events)
        
        
    def preparation(self):
        """Функция готовит объекты игрового поля."""
        self.rocket = Rocket("Rocket.png")
        self.planets = []
        self.dustclouds = []
        self.asteroids = []
        self.dv = 10
        self.objfinish = Finish("Earth.png",550, 300)
        self.planets.append(Planet("Planet2.png", 300, 300, 40, 8E+28))
        self.asteroids.append(Asteroid("Asteroid1.png", 100, 200, 40, 10))
        self.asteroids.append(Asteroid("Asteroid1.png", 500, 200, 40, 10))
        self.asteroids.append(Asteroid("Asteroid2.png", 400, 400, 40, 10))
        
class Level_3(Level): 
    def __init__(self, clock, events):
        super().__init__(clock, events)
        
        
    def preparation(self):
        """Функция готовит объекты игрового поля."""
        self.rocket = Rocket("Rocket.png")
        self.planets = []
        self.dustclouds = []
        self.asteroids = []
        self.dv = 5
        self.lenth_start_traject = 350        
        self.objfinish = Finish("Earth.png",550, 400)
        self.planets.append(Planet("Planet2.png", 300, 300, 40, 16E+28))
        self.asteroids.append(Asteroid("Asteroid1.png", 100, 200, 40, 10))
        self.asteroids.append(Asteroid("Asteroid1.png", 500, 200, 40, 10))
        self.asteroids.append(Asteroid("Asteroid2.png", 400, 400, 40, 10))
        self.asteroids.append(Asteroid("Asteroids.png", 150, 450, 40, 10))
        self.planets.append(Planet("Planet1.png", 500, 100, 40, 8E+28))
                                    
    
    
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Astro")

clock = pg.time.Clock()
menu = Menu(screen)    

menu.menufunc(clock, pg.event)

pg.quit()

