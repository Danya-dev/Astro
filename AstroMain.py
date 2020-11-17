import pygame as pg
import botton


pg.init()
pg.font.init()

SCREEN_SIZE = (800, 600)
    
class Menu():
        '''Класс меню. Реализует отрисовку меню и функции меню.'''
        def __init__(self, screen):
            self.screen = screen
            self.levels = botton.init(self.screen, [100, 50], 120, 40, (255, 0, 0), "Уровни")
            self.settings = botton.init(self.screen, [100, 100], 120, 40, (255, 0, 0), "Настройки")
            self.info = botton.init(self.screen, [100, 150], 120, 40, (255, 0, 0), "Об игре")
            self.back = botton.init(self.screen, [100, 500], 120, 40, (255, 0, 0), "Назад")
            self.position = 1
            self.level_1 = botton.init(self.screen, [100, 50], 120, 40, (255, 0, 0), "Уровень 1")
        
        def draw(self):
            screen.fill((0, 0, 0))
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.levels.click(event.pos):
                    self.position = 2
                if self.settings.click(event.pos):
                    self.position = 3
                if self.info.click(event.pos):
                    self.position = 4
                if self.back.click(event.pos):
                    self.position = 1
                
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
Menu = Menu(screen)


while not done:
    clock.tick(15)
    
    for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                
    pg.display.flip()
    Menu.draw()


pg.quit()

