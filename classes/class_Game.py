import pygame as pg
from pygame.locals import MOUSEBUTTONDOWN

from classes.class_Battlefield import Battlefield
from classes.class_Abilities import Abilities

class Game:
    def __init__(self, screen):
        self.scr = screen
        self.width = self.scr.get_width()
        self.height = self.scr.get_height()

        self.battlefield = Battlefield(self.scr)
        self.abilities = Abilities(
            self.scr,
            self.battlefield.field_x,
            self.battlefield.field_y,
            self.battlefield.field_width,
            self.battlefield.field_height
        )

    # ---------- ИЗМЕНЕНО ----------
    def handle_events(self, events):
        """Обработка событий мыши. Принимает список событий."""
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                # ПКМ — отменить выбор способности
                if event.button == 3:
                    self.abilities.cancel_selection()
                    continue

                # ЛКМ
                if event.button == 1:
                    # Сначала проверяем клик по панели способностей
                    if self.abilities.handle_click(event.pos):
                        continue

                    # Если кликнули по полю и есть активная способность
                    active = self.abilities.get_active_ability()
                    if active is None:
                        continue

                    row, col = self.battlefield.get_cell_at(event.pos)
                    if row is None:
                        continue

                    if self.battlefield.apply_ability(active, row, col):
                        self.abilities.consume_ability()

    def move(self):
        if self.battlefield.game_over:
            return
        self.battlefield.move()
        self.abilities.update_mission_points(
            self.battlefield.mission_points
        )

    def draw(self):
        self.scr.fill((0, 0, 0))
        self.battlefield.draw()
        self.abilities.draw()