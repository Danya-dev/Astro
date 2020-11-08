import pygame as pg

pg.init()
pg.font.init()

SCREEN_SIZE = (800, 600)

class button():
    pass
    
class Menu():

        
    def menufunc(self, clock, events):
        done = False
        while not done:
            clock.tick(15)
    
            for event in events.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.KEYDOWN:
                    return Level_1()
                
                
            pg.display.flip()
    
class Level():
    pass
class Level_1(Level):
    pass
    
class GameObject():
    pass

    

screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Astro")

clock = pg.time.Clock()


menu = Menu()
level = menu.menufunc(clock, pg.event)




pg.quit()

