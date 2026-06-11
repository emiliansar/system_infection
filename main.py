import pygame as pg
from pygame.display import set_mode, set_caption
from pygame.locals import QUIT

pg.init()

scr = set_mode((0, 0), pg.FULLSCREEN)
set_caption("Заражение системы")
clock = pg.time.Clock()
fps = 60

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
    
    pg.display.update()
    clock.tick(fps)

pg.quit()