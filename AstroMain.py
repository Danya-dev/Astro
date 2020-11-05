import pygame as pg

pg.init()
pg.font.init()

SCREEN_SIZE = (800, 600)

class button():
    pass
    
class menu():
    pass
    
class level():
    pass

class GameObject():
    pass

class Manager():
    pass

screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Astro")

clock = pg.time.Clock()
done = False


while not done:
    clock.tick(15)
    
    for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                
    pg.display.flip()


pg.quit()

