import pygame as pg
from pygame.display import set_mode, set_caption
from pygame.locals import QUIT

from classes.class_Game import Game

pg.init()

info = pg.display.Info()
scr = set_mode((info.current_w, info.current_h), pg.FULLSCREEN)
set_caption("Заражение системы")
clock = pg.time.Clock()
fps = 60


print(f"Screen: {scr}")
print(f"Screen type: {type(scr)}")

game = Game(scr)

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            exit()
    
    game.move()
    game.draw()
    
    pg.display.update()
    clock.tick(fps)

pg.quit()