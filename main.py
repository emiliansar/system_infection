import pygame as pg
from pygame.display import set_mode, set_caption
from pygame.locals import QUIT

from classes.class_Game import Game
from classes.class_MainMenu import MainMenu

pg.init()

info = pg.display.Info()
scr = set_mode((info.current_w, info.current_h), pg.FULLSCREEN)
set_caption("Заражение системы")
clock = pg.time.Clock()
fps = 60

print(f"Screen: {scr}")
print(f"Screen type: {type(scr)}")

# Состояния игры: 'menu', 'game'
game_state = 'menu'
main_menu = MainMenu(scr)
game = None

while True:
    events = pg.event.get()
    
    for event in events:
        if event.type == QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            exit()
    
    # ---------- ГЛАВНОЕ МЕНЮ ----------
    if game_state == 'menu':
        main_menu.draw()
        
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                action = main_menu.handle_click(event.pos)
                if action == 'play':
                    game_state = 'game'
                    game = Game(scr)
                elif action == 'quit':
                    pg.quit()
                    exit()
    
    # ---------- ИГРА ----------
    elif game_state == 'game':
        result = game.handle_events(events)
        
        # Если игрок нажал "Выход в главное меню"
        if result == 'menu':
            game_state = 'menu'
            game = None
            continue
        
        game.move()
        game.draw()
    
    pg.display.update()
    clock.tick(fps)

pg.quit()