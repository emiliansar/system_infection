import pygame as pg
from pygame.locals import MOUSEBUTTONDOWN
import subprocess
import sys
import os
from pathlib import Path
import time

from classes.class_Battlefield import Battlefield
from classes.class_Abilities import Abilities
from classes.class_VictoryScreen import VictoryScreen
from classes.class_DefeatScreen import DefeatScreen

# Путь к overlay
GAME_DIR = Path(__file__).parent.parent.resolve()
OVERLAY_DIR = GAME_DIR / 'overlay'
OVERLAY_SCRIPT = OVERLAY_DIR / 'main.py'
STATUS_FILE = OVERLAY_DIR / 'status.txt'

# Процесс overlay
_overlay_process = None
_overlay_started = False

def start_overlay():
    """Запустить overlay в отдельном процессе"""
    global _overlay_process, _overlay_started
    
    if _overlay_started and _overlay_process.poll() is None:
        return  # Уже запущен и работает
    
    try:
        STATUS_FILE.write_text('critical', encoding='utf-8')
        time.sleep(0.1)  # Даём время записать файл
        
        _overlay_process = subprocess.Popen(
            [sys.executable, str(OVERLAY_SCRIPT)],
            cwd=str(OVERLAY_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
        _overlay_started = True
        print(f"Overlay started with PID: {_overlay_process.pid}")
    except Exception as e:
        print(f"Failed to start overlay: {e}")
        import traceback
        traceback.print_exc()

def stop_overlay():
    """Остановить overlay"""
    global _overlay_process, _overlay_started
    
    if _overlay_process:
        try:
            _overlay_process.terminate()
            _overlay_process.wait(timeout=2)
            print("Overlay terminated")
        except subprocess.TimeoutExpired:
            _overlay_process.kill()
            print("Overlay killed")
        except Exception as e:
            print(f"Error stopping overlay: {e}")
        finally:
            _overlay_process = None
    
    _overlay_started = False
    
    try:
        STATUS_FILE.write_text('normal', encoding='utf-8')
    except Exception as e:
        print(f"Error writing status: {e}")

def is_overlay_running():
    """Проверить, работает ли overlay"""
    global _overlay_process
    if _overlay_process is None:
        return False
    return _overlay_process.poll() is None

class Game:
    def __init__(self, screen):
        self.scr = screen
        self.width = self.scr.get_width()
        self.height = self.scr.get_height()

        self.battlefield = Battlefield(self.scr)
        self.abilities = Abilities(
            self.scr,
            self.battlefield,
            self.battlefield.field_x,
            self.battlefield.field_y,
            self.battlefield.field_width,
            self.battlefield.field_height
        )
        self.victory_screen = VictoryScreen(self.scr)
        self.defeat_screen = DefeatScreen(self.scr)

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.abilities.cancel_selection()
                    continue

                if event.button == 1:
                    if self.battlefield.game_over:
                        action = self.victory_screen.handle_click(event.pos)
                        if action == 'restart':
                            self.restart_game()
                        elif action == 'menu':
                            return 'menu'
                        continue
                    
                    if self.battlefield.defeat:
                        action = self.defeat_screen.handle_click(event.pos)
                        if action == 'restart':
                            self.restart_game()
                        elif action == 'menu':
                            return 'menu'
                        continue
                    
                    if self.abilities.handle_click(event.pos):
                        continue

                    active = self.abilities.get_active_ability()
                    if active is None:
                        continue

                    row, col = self.battlefield.get_cell_at(event.pos)
                    if row is None:
                        continue

                    if self.battlefield.apply_ability(active, row, col):
                        self.abilities.consume_ability()
        
        return None

    def restart_game(self):
        stop_overlay()
        self.battlefield = Battlefield(self.scr)
        self.abilities = Abilities(
            self.scr,
            self.battlefield,
            self.battlefield.field_x,
            self.battlefield.field_y,
            self.battlefield.field_width,
            self.battlefield.field_height
        )

    def move(self):
        if self.battlefield.game_over:
            return
        
        if self.battlefield.defeat:
            # Запускаем overlay только один раз
            if not _overlay_started:
                start_overlay()
            # Останавливаем игру, пока overlay работает
            return
        
        self.battlefield.move()

    def draw(self):
        self.scr.fill((0, 0, 0))
        self.battlefield.draw()
        self.abilities.draw()
        
        if self.battlefield.game_over:
            self.victory_screen.draw()
        
        if self.battlefield.defeat:
            self.defeat_screen.draw()