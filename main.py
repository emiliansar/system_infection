import pygame as pg
from pygame.display import set_mode, set_caption
from pygame.locals import QUIT

from classes.class_Game import Game, stop_overlay
from classes.class_MainMenu import MainMenu
from classes.class_PauseMenu import PauseMenu

pg.init()

info = pg.display.Info()
scr = set_mode((info.current_w, info.current_h), pg.FULLSCREEN)
set_caption("Заражение системы")
clock = pg.time.Clock()
fps = 60

print(f"Screen: {scr}")
print(f"Screen type: {type(scr)}")

# Состояния игры: 'menu', 'game', 'pause'
game_state = 'menu'
main_menu = MainMenu(scr)
pause_menu = PauseMenu(scr)
game = None

while True:
    events = pg.event.get()
    
    for event in events:
        if event.type == QUIT:
            stop_overlay()  # Остановить overlay при выходе
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
                    stop_overlay()
                    pg.quit()
                    exit()
    
    # ---------- ИГРА ----------
    elif game_state == 'game':
        # Обработка ESC для паузы
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                game_state = 'pause'
                break
        
        result = game.handle_events(events)
        
        # Если игрок нажал "Выход в главное меню"
        if result == 'menu':
            stop_overlay()
            game_state = 'menu'
            game = None
            continue
        
        game.move()
        game.draw()
    
    # ---------- ПАУЗА ----------
    elif game_state == 'pause':
        # Рисуем игру на фоне (замороженную)
        game.draw()
        
        # Поверх рисуем меню паузы
        pause_menu.draw()
        
        for event in events:
            # ESC возвращает в игру
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                game_state = 'game'
                break
            
            # Обработка кликов по меню паузы
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                action = pause_menu.handle_click(event.pos)
                if action == 'continue':
                    game_state = 'game'
                elif action == 'menu':
                    stop_overlay()
                    game_state = 'menu'
                    game = None
                elif action == 'quit':
                    stop_overlay()
                    pg.quit()
                    exit()
    
    pg.display.update()
    clock.tick(fps)

stop_overlay()
pg.quit()