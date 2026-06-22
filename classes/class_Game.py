import pygame as pg
from pygame.locals import MOUSEBUTTONDOWN

from classes.class_Battlefield import Battlefield
from classes.class_Abilities import Abilities
from classes.class_VictoryScreen import VictoryScreen
from classes.class_DefeatScreen import DefeatScreen

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
        self.defeat_screen = DefeatScreen(self.scr)  # 👇 ДОБАВЛЕНО

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.abilities.cancel_selection()
                    continue

                if event.button == 1:
                    # Если игра окончена — обрабатываем клик по экрану победы
                    if self.battlefield.game_over:
                        action = self.victory_screen.handle_click(event.pos)
                        if action == 'restart':
                            self.restart_game()
                        elif action == 'menu':
                            return 'menu'
                        continue
                    
                    # 👇 ДОБАВЛЕНО: обработка экрана поражения
                    if self.battlefield.defeat:
                        action = self.defeat_screen.handle_click(event.pos)
                        if action == 'restart':
                            self.restart_game()
                        elif action == 'menu':
                            return 'menu'
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
        if self.battlefield.game_over or self.battlefield.defeat:
            return
        self.battlefield.move()

    def draw(self):
        self.scr.fill((0, 0, 0))
        self.battlefield.draw()
        self.abilities.draw()
        
        # Если игра окончена — рисуем экран победы
        if self.battlefield.game_over:
            self.victory_screen.draw()
        
        # 👇 ДОБАВЛЕНО: рисуем экран поражения
        if self.battlefield.defeat:
            self.defeat_screen.draw()