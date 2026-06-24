import pygame as pg
from pygame.display import set_mode, set_caption
from pygame.locals import QUIT

from classes.class_Game import Game, stop_overlay, write_game_status
from classes.class_MainMenu import MainMenu
from classes.class_PauseMenu import PauseMenu
from classes.class_SoundManager import SoundManager

pg.init()
pg.mixer.init()

info = pg.display.Info()
scr = set_mode((info.current_w, info.current_h), pg.FULLSCREEN)
set_caption("Заражение системы")
clock = pg.time.Clock()
fps = 60

sound_manager = SoundManager()

game_state = 'menu'
main_menu = MainMenu(scr, sound_manager)
pause_menu = PauseMenu(scr, sound_manager)
game = None

# 👇 ДВА ФЛАГА:
menu_on_start_playing = True    # нужно ли вообще играть menu_on_start
menu_on_start_launched = False  # уже ли мы его запустили

# 👇 СЧЁТЧИК КАДРОВ ДЛЯ ЛОГОВ
frame_count = 0

while True:
    events = pg.event.get()
    frame_count += 1
    
    for event in events:
        if event.type == QUIT:
            stop_overlay()
            sound_manager.stop_music()
            pg.quit()
            exit()
    
    # ---------- ГЛАВНОЕ МЕНЮ ----------
    if game_state == 'menu':
        # Останавливаем background если играет
        if sound_manager.current_music == 'background':
            sound_manager.stop_music()
        
        # 👇 ЛОГИКА С ДВУМЯ ФЛАГАМИ + ЛОГИРОВАНИЕ:
        if menu_on_start_playing:
            if not menu_on_start_launched:
                # Кадр 1: только что вошли в меню — запускаем menu_on_start
                print(f"[FRAME {frame_count}] 🔵 Запускаем menu_on_start")
                sound_manager.play_music('menu_on_start', loops=0)
                menu_on_start_launched = True  # помечаем, что запустили
                print(f"[FRAME {frame_count}] ✅ menu_on_start_launched = True")
            elif not pg.mixer.music.get_busy():
                # Последующие кадры: ждём окончания menu_on_start
                # get_busy() == False → музыка закончилась
                print(f"[FRAME {frame_count}] 🔴 menu_on_start закончился (get_busy=False)")
                print(f"[FRAME {frame_count}] 🟢 Запускаем menu_infinite")
                sound_manager.play_music('menu_infinite', loops=-1)
                menu_on_start_playing = False  # больше не играем menu_on_start
                print(f"[FRAME {frame_count}] ✅ menu_on_start_playing = False")
            else:
                # 👇 Логируем каждые 60 кадров (раз в секунду), чтобы видеть что музыка играет
                if frame_count % 60 == 0:
                    print(f"[FRAME {frame_count}] 🎵 menu_on_start играет... (get_busy={pg.mixer.music.get_busy()})")
        else:
            # menu_on_start уже отыграл — всегда играем menu_infinite
            if sound_manager.current_music != 'menu_infinite':
                print(f"[FRAME {frame_count}] 🟢 Запускаем menu_infinite (menu_on_start уже отыграл)")
                sound_manager.play_music('menu_infinite', loops=-1)
        
        main_menu.draw()
        
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                action = main_menu.handle_click(event.pos)
                if action == 'play':
                    sound_manager.play_menu_click()
                    game_state = 'game'
                    game = Game(scr, sound_manager)
                elif action == 'quit':
                    sound_manager.play_menu_click()
                    sound_manager.stop_music()
                    stop_overlay()
                    pg.quit()
                    exit()
    
    # ---------- ИГРА ----------
    elif game_state == 'game':
        if sound_manager.current_music != 'background':
            print(f"[FRAME {frame_count}] 🎵 Запускаем background")
            sound_manager.play_music('background', loops=-1)
        
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                game_state = 'pause'
                break
        
        result = game.handle_events(events)
        
        if result == 'menu':
            stop_overlay()
            write_game_status('normal')
            sound_manager.stop_music()
            game_state = 'menu'
            game = None
            continue
        
        game.move()
        game.draw()
    
    # ---------- ПАУЗА ----------
    elif game_state == 'pause':
        game.draw()
        pause_menu.draw()
        
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                game_state = 'game'
                break
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                action = pause_menu.handle_click(event.pos)
                if action == 'continue':
                    sound_manager.play_menu_click()
                    game_state = 'game'
                elif action == 'menu':
                    sound_manager.play_menu_click()
                    stop_overlay()
                    write_game_status('normal')
                    sound_manager.stop_music()
                    game_state = 'menu'
                    game = None
                elif action == 'quit':
                    sound_manager.play_menu_click()
                    sound_manager.stop_music()
                    stop_overlay()
                    pg.quit()
                    exit()
    
    pg.display.update()
    clock.tick(fps)

sound_manager.stop_music()
stop_overlay()
pg.quit()