import pygame as pg
from pygame.locals import MOUSEBUTTONDOWN

from classes.class_Battlefield import Battlefield
from classes.class_Abilities import Abilities
from classes.class_VictoryScreen import VictoryScreen

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

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.abilities.cancel_selection()
                    continue

                if event.button == 1:
                    # Если игра окончена — обрабатываем клик по окну победы
                    if self.battlefield.game_over:
                        action = self.victory_screen.handle_click(event.pos)
                        if action == 'restart':
                            self.restart_game()
                        elif action == 'menu':
                            return 'menu'  # Возвращаем сигнал для выхода в меню
                        continue
                    
                    # Обычная обработка кликов
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
        """Перезапуск игры."""
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
        self.battlefield.move()

    def draw(self):
        self.scr.fill((0, 0, 0))
        self.battlefield.draw()
        self.abilities.draw()
        
        # Если игра окончена — рисуем экран победы поверх
        if self.battlefield.game_over:
            self.victory_screen.draw()