import pygame as pg

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
                elif event.type == pg.KEYDOWN:
                    return Level_1(clock, events)
                
                
            pg.display.flip()
class Rocket():
    def __init__(self):
        self.coord = [50, 400]
        self.velocity = [0,0]
        
    def motion(self):
        self.coord[0] += self.velocity[0]
        self.coord[1] += self.velocity[1]
    
        
    def draw(self): 
        pg.draw.circle(screen, (255,255,255),
                     self.coord, 20)
        
    
class Level(): 
    pass

class Level_1(Level):
    def __init__(self,clock, events):
        self.rocket = Rocket()
        
        self.start(clock,events)
        
    def start(self, clock, events):            
        done = False
        while not done: #обработка событий
            clock.tick(15)
            screen.fill((0,0,0))
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.KEYDOWN:
                    self.rocket.velocity = (3,3)
                    self.process(clock, events)
            self.drawthemall()
            pg.display.flip()
            
    def process(self, clock, events):
            
        done = False
        while not done: #обработка событий
            clock.tick(15)
            screen.fill((0,0,0))
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
            self.movethemall()
            
            self.drawthemall()
                
                
            pg.display.flip()
        
    def drawthemall(self):
        self.rocket.draw()
        
        
    def movethemall(self):
        self.rocket.motion()
    
    
class GameObject():
    pass

    

screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Astro")

clock = pg.time.Clock()


menu = Menu()
level = menu.menufunc(clock, pg.event)




pg.quit()

