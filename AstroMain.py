import pygame as pg
import botton
import math

pg.init()
pg.font.init()

SCREEN_SIZE = (800, 600)
FPS_menu = 15
FPS = 400
dt = 100*5E+2

"""Шаг реального времени при одной иттерации цикла обработки событий игры.
Тип: float
Мера: секунды."""

scale_param = 5E+8
"""Масштабирование экранных координат по отношению к физическим.
Тип: float
Мера: количество пикселей на один метр."""
RIGHT = "turn to the right"
LEFT = "turn to the left"
UP = "speed up"
DOWN = "speed down"
STOP = "not turn"


DIRECTION = 'textures/'
LEVELDIRECTION = 'sketches/'
canvas = pg.Surface(SCREEN_SIZE)
window = pg.display.set_mode((SCREEN_SIZE))
space = pg.image.load(DIRECTION + "space5.png").convert_alpha()
screenpos = (0, 0)

def stringhelper(s : str):
        s = s[1: len(s)-2]
        number1, coma, number2 = s.partition(',')
        return [int(number1), int(number2)]  
  
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
        """Класс меню. Реализует отрисовку меню и функции меню."""
        def __init__(self, screen):
            self.screen = screen
            self.levels = botton.Botton_image(self.screen, [90 , 513],
                                              DIRECTION + "play.png",
                                              "circle")
            self.settings = botton.Botton_image(self.screen, [184 , 540], 
                                                DIRECTION + "settings.png",
                                                "circle")
            self.back = botton.Botton(self.screen, [100, 100], 120, 40,
                                       (0, 0, 0), "Назад")
            self.position = 1  
            """Позиция меню. 1 - главное, 2 - уровни, 3 - настройки,
            4 - переход к уровню."""
            self.level_1 = botton.Botton_image(self.screen, [61, 487],
                                               DIRECTION +  "level_1.png",
                                               "rect")
            self.level_2 = botton.Botton_image(self.screen, [117 , 495],
                                                DIRECTION + "level_2.png",
                                                "rect")
            self.level_3 = botton.Botton_image(self.screen, [173 , 496],
                                                DIRECTION + "level_3.png",
                                                "rect")
            self.sett = botton.Botton(self.screen, [160, 150], 240, 40,
                                         (0, 0, 0), "Всё уже настроено!")
            self.menufunc(clock, pg.event)
        
        
        def menufunc(self, clock, events):
            """Функция, обрабатывающая события в режиме открытого меню."""
            done = False
            while not done:
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
                            if self.level_1.click(event.pos):
                                return Level_1(clock, events,
                                               LEVELDIRECTION, 'level1.txt')
                            elif self.level_2.click(event.pos):
                                return Level_2(clock, events, None, None)
                            elif self.level_3.click(event.pos): 
                                return Level_3(clock, events, None, None)
                        else:   
                            if self.back.click(event.pos):
                                self.position = 1   
                    elif event.type == pg.KEYDOWN:
                        if self.position == 2 and event.key == pg.K_p:
                            return DeveloperMode()
                pg.display.flip()
                self.draw()
        
        
        def draw(self):
            """Функция, отрисовывающая меню."""
            screen.blit(space, screenpos)
            if self.position == 1:
                self.levels.draw()
                self.settings.draw()
            if self.position == 2:
                self.level_1.draw()
                self.level_2.draw()
                self.level_3.draw()
            if self.position == 3:
                self.sett.draw()

    
        
        def levels(self):
            pass
            
           
        def setting(self):
            pass
            
            
        def info(self):
            pass
        
        
class DeveloperMode():
    """Класс разработки уровней."""
    class GameObject():
        """Класс игрового объекта, который размещает разработчик."""
        def __init__(self, image, name, objtype):
            self.image = image
            """Изображение игрового объекта."""
            
            self.name = name
            """Имя игрового объекта."""
            
            self.objtype = objtype
            """Тип игрового объекта"""
            
            self.w, self.h = self.image.get_size()
            """Размеры изображения игрового объекта."""
            
            
    def __init__(self):
        self.planet1 = self.GameObject(
            pg.image.load(DIRECTION + "Planet1.png").convert_alpha(),
                                      'Planet1', 'planet')
        """Добавление планеты первого типа."""
        
        self.planet2 = self.GameObject(
            pg.image.load(DIRECTION + "Planet2.png").convert_alpha(),
                                      'Planet2', 'planet')
        """Добавление планеты второго типа."""
        
        self.finish = self.GameObject(
            pg.image.load(DIRECTION + "Earth.png").convert_alpha(),
                                      'finish' ,'finish')
        """Добавление финиша."""
        
        self.asteroid1 = self.GameObject(
            pg.image.load(DIRECTION + "Asteroid1.png").convert_alpha(),
                                         'Asteroid1', 'asteroid')
        """Добавление астероида первого типа."""
        
        self.asteroid2 = self.GameObject(
            pg.image.load(DIRECTION + "Asteroid2.png").convert_alpha(),
                                         'Asteroid2', 'asteroid')
        self.rocket = self.GameObject(
            pg.image.load(DIRECTION + "Rocket.png").convert_alpha(),
                                      'rocket', 'rocket')
        self.delete = self.GameObject(
            pg.image.load(DIRECTION + "Rocket.png"), 'Delete', 'Delete')
        """Добавление финиша."""
        
        self.planetcash = []
        """Лист добавляемых планет."""
        
        self.rfcash = [(400, 300), (600,300)]
        """Лист координат ракеты и финиша соответственно."""
        
        self.asteroidscash = []
        """Лист добавляемых астероидов."""
        
        self.process(pg.event)
        
        
    def process(self,events):
        """Функция"""
        done = False
        gmobject = self.finish # Объект, с которым работает разработчик.  
        workname = 'finish' # Тип объекта, с которым работает разработчик.
        while not done:
            clock.tick(30 )
            screen.blit(space, screenpos)            
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.MOUSEBUTTONDOWN :  
                    if event.button == 1:                    
                        if gmobject.name == workname:
                            if workname == 'Delete':
                                self.deleteobj(event)
                            else:   
                                pos = [0, 0]
                                pos[0] = int( event.pos[0] - gmobject.w / 2)
                                pos[1] = int(event.pos[1] - gmobject.h / 2)                               
                                self.cashing(gmobject, pos)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.constructor()
                        done = True
                    elif event.key == pg.K_p:
                        workname = 'planet'
                        print(gmobject.name)
                    elif event.key == pg.K_f:
                        gmobject = self.finish
                        workname = gmobject.name
                        print(gmobject.name)
                    elif event.key == pg.K_r:
                        gmobject = self.rocket
                        workname = gmobject.name
                        print(gmobject.name)
                    elif event.key == pg.K_m:
                        workname = 'asteroid'
                        print(gmobject.name)
                    elif event.key == pg.K_1:
                        if workname == 'planet':
                            gmobject = self.planet1
                            workname = self.planet1.name
                            print(gmobject.name)
                        elif workname == 'asteroid':
                            gmobject = self.asteroid1
                            workname = self.asteroid1.name
                            print(gmobject.name)
                    elif event.key == pg.K_2:
                        if workname == 'planet':
                            gmobject = self.planet2
                            workname = self.planet2.name
                            print(gmobject.name)
                        elif workname == 'asteroid':
                            gmobject = self.asteroid2
                            workname = self.asteroid2.name
                            print(gmobject.name)
                    elif event.key == pg.K_BACKSPACE:
                        gmobject = self.delete
                        workname = self.delete.name
                        print(gmobject.name)
            self.draw()           
            pg.display.flip()
            
            
    def deleteobj(self, event):
        for gmobject in self.planetcash:
            x = gmobject[1][0]
            y = gmobject[1][1]
            if (x < event.pos[0] < x + gmobject[2]) and (
                    y < event.pos[1] < y + gmobject[3]):
                self.planetcash.remove(gmobject)
        for gmobject in self.asteroidscash:
            x = gmobject[1][0]
            y = gmobject[1][1]
            if (x < event.pos[0] < x + gmobject[2]) and (
                    y < event.pos[1] < y + gmobject[3]):
                self.asteroidscash.remove(gmobject)
                
                
                
    def cashing(self, gmobject, pos):
        if gmobject.objtype == 'planet':
            self.planetcash.append([gmobject.name, pos,
                                    gmobject.w, gmobject.h ])
            print(self.planetcash[len(self.planetcash)-1])
        elif gmobject.objtype == 'finish':
            self.rfcash[1] = pos
        elif gmobject.objtype == 'rocket':
            self.rfcash[0] = pos
        elif gmobject.objtype == 'asteroid':
            self.asteroidscash.append([gmobject.name, pos,
                                       gmobject.w, gmobject.h])
        print( self.planetcash)

            
            
    def draw(self):
        for planet in self.planetcash:
            screen.blit(pg.image.load(DIRECTION + planet[0] + '.png'),
                        planet[1])
          
        for asteroid in self.asteroidscash:
            screen.blit(pg.image.load(DIRECTION + asteroid[0] + '.png'),
                        asteroid[1])
        screen.blit(self.rocket.image, self.rfcash[0])
        screen.blit(self.finish.image, self.rfcash[1])
        
            
    def constructor(self):
        direction = 'sketches/'
        print('введите название уровня')
        name = input()
        newlevel = open(direction + name + '.txt', 'w') 
        newlevel.write('Rocket:' + '\n')
        newlevel.write(str(self.rfcash[0]) + '\n')
        newlevel.write('\n')
        newlevel.write('Finish:' + '\n')
        newlevel.write(str(self.rfcash[1]) + '\n')
        newlevel.write('\n')
        newlevel.write('planets:' + '\n')
        for planet in self.planetcash:
            newlevel.write(planet[0] + '\n')
            newlevel.write(str(planet[1]) + '\n')
        newlevel.write('\n')
        newlevel.write('asteroids:' + '\n')
        for asteroid in self.asteroidscash:
            newlevel.write(asteroid[0] + '\n')
            newlevel.write(str(asteroid[1]) + '\n')
        newlevel.write('\n')
        newlevel.close()

        
class Rocket(pg.sprite.Sprite):
    """Класс ракеты."""
    def __init__(self, filename, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(DIRECTION + filename).convert_alpha()
        """Изображение ракеты."""
        
        self.w , self.h = self.image.get_size()
        """Ширина и высота изображения ракеты"""
        
        self.coord = pos
        """Координаты на экране в пикселах."""
        
        self.coord0 = [pos[0], pos[1]]
        """Стартовые координаты в пикселах."""
        
        self.real_coord = [self.coord[0]*scale_param, 
                           self.coord[1]*scale_param] 
        """Координаты пространстве."""
        
        self.rect = self.image.get_rect(center=(self.coord[0], self.coord[1]))
        """Экземпляр класса Rect, ширина и высота которого совпадают
        с таковыми у изображения ракеты."""
        
        self.mask = pg.mask.from_surface(self.image)
        """Маска ракеты."""
        
        self.angle = 0
        """Угол, наклона оси ракеты к оси x (ось x - направлена вправо)."""
        
        self.velocity = [0,0]
        """Скорость ракеты."""
        
        self.upfire = pg.image.load(
            DIRECTION + "upfire1.png").convert_alpha()
        """Изображение ракеты c включенным двигателем поворота направо."""
        
        self.downfire = pg.image.load(
            DIRECTION + "downfire1.png").convert_alpha()
        """Изображение ракеты c включенным двигателем поворота налево."""
        
        self.fullfire = pg.image.load(
            DIRECTION + "fullfire1.png").convert_alpha()
        """Изображение ракеты c включенными двигателеми тяги вперёд."""
        
        self.frontfire = pg.image.load(
            DIRECTION + "frontfire1.png").convert_alpha()
        """Изображение ракеты c включенными двигателеми тяги назад."""
    
    
    def motion(self):
        """Функция движения ракеты."""
        self.findangle(self.velocity)
        self.coord[0] = int(self.real_coord[0] / scale_param)
        self.coord[1] = int(self.real_coord[1] / scale_param)
        self.rect = self.image.get_rect(center=(self.coord[0],
                                                self.coord[1]))
        
    
    def findangle(self, direction):
        """Функция, поворачивающая ракету в напрвлении движения."""
        if direction[0] > 0:
           self.angle = math.degrees(math.atan2(-direction[1], direction[0]))
        if direction[0] < 0:
           self.angle = math.degrees(-math.atan2(
               -direction[1], -direction[0]) - math.pi)   
           
   
    def draw(self, surf, image, topleft, angle):
        """Функция, отрисовывающая ракету на экране."""
        image.blit(self.upfire, topleft)
        rotated_image = pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(
            center = image.get_rect(topleft = topleft).center)
        surf.blit(rotated_image, new_rect.topleft)
        #pg.draw.rect(surf, (255, 0, 0), new_rect, 2)
            
    
    def gravity(self, planets): 
        """Функция, реализующая изменение скорости ракеты под
        действием гравитационных сил других объектов игрового поля."""
        z = runge_kutta(self.real_coord, self.velocity, planets)
        self.real_coord = z[0]
        self.velocity = z[1]


    def trajectory(self, planets, n):
        """Функция, отрисовывающая траекторию по которой будет
        двигаться ракета, если двигатели не будут работать."""
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
        """Функция, реализующая работу двигателей. Изменяет скорость
        ракеты в соответсвие с работой двигателей, а также отрисовывает
        выброс продуктов сгорания топлива."""
        if motion == LEFT:
            self.velocity[0] -= dv * math.sin(math.radians(self.angle))
            self.velocity[1] -= dv * math.cos(math.radians(self.angle))
            return self.downfire
        elif motion == RIGHT:
            self.velocity[0] += dv * math.sin(math.radians(self.angle))
            self.velocity[1] += dv * math.cos(math.radians(self.angle))
            return self.upfire
        elif motion == UP:
            self.velocity[0] += dv * math.cos(math.radians(self.angle))
            self.velocity[1] -= dv * math.sin(math.radians(self.angle))
            return self.fullfire
        elif motion == DOWN:
            if self.velocity[0]**2 + self.velocity[1]**2 <= 10000:
                return self.image
            else:
                self.velocity[0] -= dv * math.cos(math.radians(self.angle))
                self.velocity[1] += dv * math.sin(math.radians(self.angle))
                return self.frontfire            
        elif motion == STOP:
            return self.image

        
class Planet(pg.sprite.Sprite): 
    """Класс планет."""
    def __init__(self, filename, pos, rad, mass):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.coord = pos  # Координаты на экране в пикселах.
        self.real_coord = [pos[0]*scale_param,
                           pos[1]*scale_param]  # Координаты в пространстве.  
        self.rad = rad
        self.mass = mass
        self.mask = pg.mask.from_surface(self.image)
    
    
    def draw(self, x, y):
        self.rect = self.image.get_rect(
            center=(x + self.coord[0], y + self.coord[1]))
        screen.blit(self.image, self.rect)
        
        
class Asteroid(pg.sprite.Sprite):
    """Класс астероидов."""
    def __init__(self, filename, pos, rad, mass):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.coord = pos  # Координаты на экране в пикселах.
        self.real_coord = [pos[0]*scale_param,
                           pos[1]*scale_param]  # Координаты в пространстве.  
        self.rad = rad
        self.mass = mass        
        self.mask = pg.mask.from_surface(self.image)
    
    
    def draw(self, x, y):
        """Функция, отрисовывающая астероид на экране."""
        self.rect = self.image.get_rect(
            center=(x + self.coord[0], y + self.coord[1]))
        screen.blit(self.image, self.rect)
        
        
        
class Finish(pg.sprite.Sprite):
    def __init__(self, filename, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(DIRECTION + filename).convert_alpha()
        self.coord = pos  # Координаты на экране в пикселах.       
        self.rect = self.image.get_rect(center=(self.coord[0], self.coord[1]))
        self.mask = pg.mask.from_surface(self.image)
    
    
    def draw(self, x, y):
        self.rect = self.image.get_rect(
            center=(x + self.coord[0], y + self.coord[1]))
        screen.blit(self.image, self.rect)


class Level():
    """Класс уровня. Регулирует действия программы после переходу к уровню."""
    def __init__(self, clock, events, direction, filename):
        self.dv = 20
        self.width = 30
        self.lenth_start_traject = 150
        gamegoes = True
        pg.mouse.set_visible(False)
        while gamegoes:
            self.preparation(direction, filename)
            self.start(clock, events)
            gamegoes = self.process(clock, events)

        pg.mouse.set_visible(True)
        return Menu(screen)      

            
            
    def preparation(self,direction, filename):
        """Функция готовит объекты игрового поля."""
        self.planets = []
        self.asteroids = []
        level = open(direction + filename, 'r')
        level.readline()
        self.rocket = Rocket("Rocket.png",
                             stringhelper(level.readline()))
        level.readline()
        print(level.readline())
        self.objfinish = Finish("Earth.png",stringhelper(level.readline()))
        level.readline()
        level.readline()
        line = level.readline()
        print(line)
        while not(line == '\n'):
            name = line[0: len(line)-1]
            line = level.readline()
            print(line)
            self.planets.append(Planet(DIRECTION + name + '.png',
                                stringhelper(line), 40, 8E+28))
            line = level.readline()
            print(line)            
        level.readline()
        line = level.readline()
        print(line)
        while not(line == '\n'):
            self.asteroids.append(Asteroid(
                DIRECTION + line[0: len(line)-1] + '.png',
                stringhelper(level.readline()), 40, 10))
            line = level.readline()
        level.close()
            


                
      
    def start(self, clock, events):
        """Функция обрабатывает запуск ракеты."""
        done = False
        launchbool = False
        force = 50
        rocdirect = [1,0]
        mouse_coord = self.rocket.coord0
        trajectory = False
        while not done: # Обработка событий.
            clock.tick(30)
            screen.blit(space, screenpos)            
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.KEYDOWN: 
                    if event.key == pg.K_p:
                        prgo = True
                        while prgo:
                            prgo = self.preview(clock, events)
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
            x = - self.rocket.coord[0] + self.rocket.coord0[0] 
            y = - self.rocket.coord[1] + self.rocket.coord0[1]
            self.drawthemall(self.rocket.image, x, y)
            pg.display.flip()
        
        
    def preview(self, clock, events):
        """Функция предпросмотра уровня.""" 
        done = False
        (f1, f2, f3, f4) = (False, False, False, False)
        (x, y) = (0, 0)
        image = self.rocket.image
        while not done: 
            clock.tick(FPS)
            screen.blit(space, screenpos)
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.KEYDOWN: 
                    if (event.key == pg.K_LEFT) or (event.key == pg.K_a):
                        f1 = True
                    if (event.key == pg.K_RIGHT) or (event.key == pg.K_d):
                        f2 = True
                    if (event.key == pg.K_UP) or (event.key == pg.K_w):
                        f3 = True
                    if (event.key == pg.K_DOWN) or (event.key == pg.K_s):
                        f4 = True
                    if event.key == pg.K_p:
                        return False
                elif event.type == pg.KEYUP: 
                    if (event.key == pg.K_LEFT) or (event.key == pg.K_a):
                        f1 = False
                    if (event.key == pg.K_RIGHT) or (event.key == pg.K_d):
                        f2 = False
                    if (event.key == pg.K_UP) or (event.key == pg.K_w):
                        f3 = False
                    if (event.key == pg.K_DOWN) or (event.key == pg.K_s):
                        f4 = False
            if f1:
                x += 1
            if f2:
                x -= 1
            if f3:
                y += 1
            if f4:
                y -= 1
            self.drawthemall(image, x, y)
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
                        return True
                    elif (event.key == pg.K_SPACE) or (
                            event.key == pg.K_ESCAPE):
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
                                    elif(event.key == pg.K_SPACE) or (
                                            event.key == pg.K_ESCAPE):
                                        i = 1  
                                        done = False
                    elif (event.key == pg.K_LEFT) or (event.key == pg.K_a):
                        motion = LEFT
                    elif (event.key == pg.K_RIGHT) or (event.key == pg.K_d):
                        motion = RIGHT
                    elif (event.key == pg.K_UP) or (event.key == pg.K_w):
                        motion = UP
                    elif (event.key == pg.K_DOWN) or (event.key == pg.K_s):
                        motion = DOWN
                elif event.type == pg.KEYUP:

                    if event.key in [pg.K_LEFT,pg.K_a,pg.K_d, pg.K_w, pg.K_s,
                                 pg.K_RIGHT, pg.K_DOWN, pg.K_UP]:
                      
                        motion = STOP
            image = self.rocket.activate(motion, self.dv)
            x = - self.rocket.coord[0] + self.rocket.coord0[0] 
            y = - self.rocket.coord[1] + self.rocket.coord0[1]
            self.rocket.gravity(self.planets)
            self.rocket.trajectory(self.planets, 150)
            self.movethemall()
            self.drawthemall(image, x, y)
            if self.oncollision():
                return True
            if self.finish():
                return False

            pg.display.flip()
       
        

    def drawthemall(self, image, x, y):
        """Функция реализует отрисовку объектов игрового поля.
        Учитывает перемещение ракеты, чтобы она оставалась в определённом
        месте на экране.""" 
        
        for planet in self.planets:
            planet.draw(x, y)
        for asteroid in self.asteroids :
            asteroid.draw(x, y)
        corner_cords = [x + self.rocket.coord[0] - self.rocket.w/2,
                        y + self.rocket.coord[1] - self.rocket.h/2]
        self.rocket.draw(screen, image, corner_cords, self.rocket.angle)
        screen.blit(self.objfinish.image, self.objfinish.rect)
        self.objfinish.draw(x, y)
      
        
    def movethemall(self):
        """Функция перемещает объекты игрового поля.""" 
        self.rocket.motion()      
        
        
    def oncollision(self):
        """Функция обрабатывает столкновения ракеты
        с объектами игрового поля.""" 
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
        """Функция обрабатывает прилёт ракеты в пункт назначения.""" 
        r1 = int(self.rocket.coord[0] - self.rocket.image.get_width()/2)
        r2 = int(self.rocket.coord[1] - self.rocket.image.get_height()/2)
        a1 = int(
            self.objfinish.coord[0] - self.objfinish.image.get_width()/2)
        a2 = int(
            self.objfinish.coord[1] - self.objfinish.image.get_height()/2)
        offset = (r1 - a1, r2 - a2)
        if self.objfinish.mask.overlap_area(self.rocket.mask, offset) > 0:
            return True
        
class Level_1(Level):
    """Класс 1 уровня. Регулирует действия программы после переходу к 3 уровню.
    Наследует методы класса Level."""
    def __init__(self, clock, events, direction, filename):
        super().__init__(clock, events, direction, filename)

        
class Level_2(Level):
    """Класс 2 уровня. Регулирует действия программы после переходу к 3 уровню.
    Наследует методы класса Level."""
    def __init__(self, clock, events, direction, filename):
        super().__init__(clock, events, direction, filename)
        
        
    def preparation(self, direction, filename):
        """Функция готовит объекты игрового поля."""
        self.rocket = Rocket("Rocket.png",[100, 300])
        self.planets = []
        self.asteroids = []
        self.dv = 10
        self.objfinish = Finish("Earth.png",[550, 300])
        self.planets.append(
            Planet(DIRECTION + "Planet2.png", [300, 300], 40, 8E+28))
        self.asteroids.append(
            Asteroid(DIRECTION + "Asteroid1.png", [100, 200], 40, 10))
        self.asteroids.append(
            Asteroid(DIRECTION + "Asteroid1.png", [500, 200], 40, 10))
        self.asteroids.append(
            Asteroid(DIRECTION + "Asteroid2.png", [400, 400], 40, 10))
        
class Level_3(Level): 
    """Класс 3 уровня. Регулирует действия программы после переходу к 3 уровню.
    Наследует методы класса Level."""
    def __init__(self, clock, events, direction, filename):
        super().__init__(clock, events, direction, filename)
        
        
    def preparation(self, direction, filename):
        """Функция готовит объекты игрового поля."""
        self.rocket = Rocket("Rocket.png", [100, 300])
        self.planets = []
        self.dustclouds = []
        self.asteroids = []
        self.dv = 5
        self.lenth_start_traject = 350        
        self.objfinish = Finish("Earth.png",[550, 400])
        self.planets.append(
            Planet(DIRECTION + "Planet2.png", [300, 300], 40, 16E+28))
        self.asteroids.append(
            Asteroid(DIRECTION + "Asteroid1.png", [100, 200], 40, 10))
        self.asteroids.append(
            Asteroid(DIRECTION + "Asteroid1.png", [500, 200], 40, 10))
        self.asteroids.append(
            Asteroid(DIRECTION + "Asteroid2.png", [400, 400], 40, 10))
        self.asteroids.append(
            Asteroid(DIRECTION + "Asteroids.png", [150, 450], 40, 10))
        self.planets.append(
            Planet(DIRECTION + "Planet1.png", [500, 100], 40, 8E+28))
                                    
     
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Astro")

clock = pg.time.Clock()
menu = Menu(screen)    



pg.quit()
