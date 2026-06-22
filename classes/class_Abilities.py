import pygame as pg
from icecream import ic

class Abilities:
    def __init__(
        self, screen,
        battlefield,  # 👈 ДОБАВЛЕНО: передаём Battlefield
        field_x,
        field_y,
        field_width,
        field_height
    ):
        self.scr = screen
        self.battlefield = battlefield  # 👈 СОХРАНЯЕМ ссылку
        self.field_x = field_x
        self.field_y = field_y
        self.field_width = field_width
        self.field_height = field_height
        
        self.panel_x = field_x + field_width + 50
        self.panel_y = field_y
        self.panel_width = 250
        self.panel_height = 450
        
        # 👇 УБРАНО: self.mission_points = 0
        self.active_ability = None
        
        self.abilities = {
            'delete_1': {'name': 'Удалить 1', 'cost': 5, 'size': 1},
            'delete_9': {'name': 'Удалить 9', 'cost': 5, 'size': 3},
            'reset':    {'name': 'Сброс',     'cost': 5, 'size': None},
        }
        
        self.font_title = pg.font.Font(None, 36)
        self.font_text = pg.font.Font(None, 28)
    
    def draw(self):
        pg.draw.rect(self.scr, (30, 30, 30), (self.panel_x, self.panel_y, self.panel_width, self.panel_height))
        pg.draw.rect(self.scr, (100, 100, 100), (self.panel_x, self.panel_y, self.panel_width, self.panel_height), 2)
        
        title = self.font_title.render("Очки миссии", True, (255, 255, 255))
        self.scr.blit(title, (self.panel_x + 20, self.panel_y + 20))

        # 👇 ИЗМЕНЕНО: получаем очки напрямую из Battlefield
        points_text = self.font_title.render(f"{self.battlefield.mission_points}", True, (0, 255, 0))
        self.scr.blit(points_text, (self.panel_x + 20, self.panel_y + 60))
        
        y_offset = self.panel_y + 180
        for key, ability in self.abilities.items():
            btn_color = (50, 50, 50) if self.active_ability != key else (0, 100, 0)
            pg.draw.rect(self.scr, btn_color, (self.panel_x + 20, y_offset, self.panel_width - 40, 60))
            pg.draw.rect(self.scr, (100, 100, 100), (self.panel_x + 20, y_offset, self.panel_width - 40, 60), 1)

            name_text = self.font_text.render(ability['name'], True, (255, 255, 255))
            cost_text = self.font_text.render(f"{ability['cost']} оч.", True, (255, 200, 0))
            
            self.scr.blit(name_text, (self.panel_x + 30, y_offset + 10))
            self.scr.blit(cost_text, (self.panel_x + 30, y_offset + 35))
            
            y_offset += 80
    
    # 👇 УБРАНО: update_mission_points()

    def handle_click(self, pos):
        mx, my = pos
        
        if not (self.panel_x <= mx <= self.panel_x + self.panel_width and
                self.panel_y <= my <= self.panel_y + self.panel_height):
            return False
        
        y_offset = self.panel_y + 180
        for key, ability in self.abilities.items():
            btn_rect = pg.Rect(self.panel_x + 20, y_offset, self.panel_width - 40, 60)
            if btn_rect.collidepoint(mx, my):
                # 👇 ИЗМЕНЕНО: проверяем очки в Battlefield
                if self.battlefield.mission_points >= ability['cost']:
                    if self.active_ability == key:
                        self.active_ability = None
                    else:
                        self.active_ability = key
                return True
            y_offset += 80
        
        return False

    def get_active_ability(self):
        return self.active_ability

    def get_ability_cost(self, key):
        return self.abilities[key]['cost']

    def consume_ability(self):
        if self.active_ability is None:
            return
        cost = self.abilities[self.active_ability]['cost']
        # 👇 ИЗМЕНЕНО: уменьшаем очки в Battlefield
        self.battlefield.mission_points -= cost
        self.active_ability = None

    def cancel_selection(self):
        self.active_ability = None