# import pygame as pg
# from icecream import ic

# class Abilities:
#     def __init__(
#         self, screen,
#         field_x,
#         field_y,
#         field_width,
#         field_height
#     ):
#         self.scr = screen
#         self.field_x = field_x
#         self.field_y = field_y
#         self.field_width = field_width
#         self.field_height = field_height
        
#         self.panel_x = field_x + field_width + 50
#         self.panel_y = field_y
#         self.panel_width = 250
#         self.panel_height = 400
        
#         self.mission_points = 0
#         self.active_ability = None
        
#         self.abilities = {
#             'delete_1': {'name': 'Удалить 1', 'cost': 5, 'size': 1},
#             'delete_9': {'name': 'Удалить 9', 'cost': 5, 'size': 3},
#             'reset': {'name': 'Сброс', 'cost': 5, 'size': None},
#         }
        
#         self.font_title = pg.font.Font(None, 36)
#         self.font_text = pg.font.Font(None, 28)
    
#     def draw(self):
#         pg.draw.rect(self.scr, (30, 30, 30), (self.panel_x, self.panel_y, self.panel_width, self.panel_height))
#         pg.draw.rect(self.scr, (100, 100, 100), (self.panel_x, self.panel_y, self.panel_width, self.panel_height), 2)
        
#         title = self.font_title.render("Очки миссии", True, (255, 255, 255))
#         self.scr.blit(title, (self.panel_x + 20, self.panel_y + 20))

#         points_text = self.font_title.render(f"{self.mission_points}", True, (0, 255, 0))
#         self.scr.blit(points_text, (self.panel_x + 20, self.panel_y + 60))
        
#         y_offset = self.panel_y + 180
#         ic(self.abilities.items())
#         for key, ability in self.abilities.items():
#             ic(f"Способность {ability} заспавнена")
            
#             btn_color = (50, 50, 50) if self.active_ability != key else (0, 100, 0)
#             pg.draw.rect(self.scr, btn_color, (self.panel_x + 20, y_offset, self.panel_width - 40, 60))
#             pg.draw.rect(self.scr, (100, 100, 100), (self.panel_x + 20, y_offset, self.panel_width - 40, 60), 1)

#             name_text = self.font_text.render(ability['name'], True, (255, 255, 255))
#             cost_text = self.font_text.render(f"{ability['cost']} оч.", True, (255, 200, 0))
            
#             self.scr.blit(name_text, (self.panel_x + 30, y_offset + 10))
#             self.scr.blit(cost_text, (self.panel_x + 30, y_offset + 35))
            
#             # 👇 ДОБАВИТЬ ЭТУ СТРОКУ — сдвиг вниз на 80px после каждой кнопки
#             y_offset += 80
    
#     def update_mission_points(self, points):
#         self.mission_points = points

import pygame as pg
from icecream import ic

class Abilities:
    def __init__(
        self, screen,
        field_x,
        field_y,
        field_width,
        field_height
    ):
        self.scr = screen
        self.field_x = field_x
        self.field_y = field_y
        self.field_width = field_width
        self.field_height = field_height
        
        self.panel_x = field_x + field_width + 50
        self.panel_y = field_y
        self.panel_width = 250
        self.panel_height = 450  # чуть увеличил, чтобы все кнопки влезли
        
        self.mission_points = 0
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

        points_text = self.font_title.render(f"{self.mission_points}", True, (0, 255, 0))
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
    
    def update_mission_points(self, points):
        self.mission_points = points

    # ---------- НОВОЕ ----------
    def handle_click(self, pos):
        """
        Обрабатывает клик мыши по панели способностей.
        Возвращает True, если клик попал по какой-либо кнопке (чтобы
        событие не передавалось дальше, например на поле битвы).
        """
        mx, my = pos
        
        # Клик вне панели — игнорируем
        if not (self.panel_x <= mx <= self.panel_x + self.panel_width and
                self.panel_y <= my <= self.panel_y + self.panel_height):
            return False
        
        y_offset = self.panel_y + 180
        for key, ability in self.abilities.items():
            btn_rect = pg.Rect(self.panel_x + 20, y_offset, self.panel_width - 40, 60)
            if btn_rect.collidepoint(mx, my):
                # Проверяем хватает ли очков
                if self.mission_points >= ability['cost']:
                    # Повторный клик по той же кнопке — снимаем выбор
                    if self.active_ability == key:
                        self.active_ability = None
                    else:
                        self.active_ability = key
                return True
            y_offset += 80
        
        return False

    def get_active_ability(self):
        """Возвращает ключ выбранной способности или None."""
        return self.active_ability

    def get_ability_cost(self, key):
        return self.abilities[key]['cost']

    def consume_ability(self):
        """Списывает очки и снимает выбор после успешного применения."""
        if self.active_ability is None:
            return
        cost = self.abilities[self.active_ability]['cost']
        self.mission_points -= cost
        self.active_ability = None

    def cancel_selection(self):
        """Снять выбор способности (например, по ПКМ)."""
        self.active_ability = None