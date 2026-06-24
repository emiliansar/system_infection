import pygame as pg
from icecream import ic
from pathlib import Path

class Abilities:
    def __init__(
        self, screen,
        battlefield,
        field_x,
        field_y,
        field_width,
        field_height
    ):
        self.scr = screen
        self.battlefield = battlefield
        self.field_x = field_x
        self.field_y = field_y
        self.field_width = field_width
        self.field_height = field_height
        
        self.panel_x = field_x + field_width + 50
        self.panel_y = field_y
        self.panel_width = 280
        self.panel_height = 450
        
        self.active_ability = None
        
        self.abilities = {
            'delete_1': {'name': 'Удалить один', 'cost': 5, 'size': 1},
            'delete_9': {'name': 'Удалить в радиусе', 'cost': 5, 'size': 3},
            'reset':    {'name': 'Сброс системы',     'cost': 5, 'size': None},
        }
        
        # Шрифты
        self.font_title = pg.font.Font(None, 48)
        self.font_subtitle = pg.font.Font(None, 32)
        self.font_text = pg.font.Font(None, 28)
        
        # Позиции
        self.bar_width = 240
        self.bar_height = 10
        self.ability_spacing = 110
        self.first_ability_y = self.panel_y + 100
        
        # Размер иконок
        self.icon_size = 24
        
        # Загрузка иконок из папки images/
        self.images_dir = Path(__file__).parent.parent / 'images'
        self._load_icons()
    
    def _load_icons(self):
        """Загружает иконки способностей из папки images/"""
        # Иконка корзины (для delete_1)
        self.icon_delete = pg.image.load(str(self.images_dir / 'abilities_delete.png')).convert_alpha()
        self.icon_delete = pg.transform.smoothscale(self.icon_delete, (self.icon_size, self.icon_size))
        
        # Иконка радара (для delete_9)
        self.icon_radar = pg.image.load(str(self.images_dir / 'abilities_radar.png')).convert_alpha()
        self.icon_radar = pg.transform.smoothscale(self.icon_radar, (self.icon_size, self.icon_size))
        
        # Иконка плюса (для delete_9)
        self.icon_plus = pg.image.load(str(self.images_dir / 'abilities_plus.png')).convert_alpha()
        self.icon_plus = pg.transform.smoothscale(self.icon_plus, (self.icon_size, self.icon_size))
        
        # Иконка жёсткого диска (для reset)
        self.icon_harddisk = pg.image.load(str(self.images_dir / 'abilities_harddisk.png')).convert_alpha()
        self.icon_harddisk = pg.transform.smoothscale(self.icon_harddisk, (self.icon_size, self.icon_size))
        
        print("[ABILITIES] Icons loaded successfully")
    
    def draw(self):
        # Очищаем фон панели
        self.scr.fill((0, 0, 0), (self.panel_x, self.panel_y, self.panel_width, self.panel_height))
        
        # Заголовок "Способности"
        title = self.font_title.render("Способности", True, (255, 255, 255))
        self.scr.blit(title, (self.panel_x + 20, self.panel_y + 10))
        
        # Очки
        points_text = self.font_subtitle.render(f"Очки: {self.battlefield.mission_points}", True, (255, 255, 255))
        self.scr.blit(points_text, (self.panel_x + 20, self.panel_y + 60))
        
        # Рисуем способности
        y_offset = self.first_ability_y
        for i, (key, ability) in enumerate(self.abilities.items()):
            is_active = self.active_ability == key
            can_afford = self.battlefield.mission_points >= ability['cost']
            
            # Название способности + иконки
            name_color = (255, 255, 0) if is_active else (255, 255, 255)
            name_text = self.font_text.render(ability['name'], True, name_color)
            
            # Позиция для текста
            text_x = self.panel_x + 20
            text_y = y_offset
            
            # Рисуем иконки слева от текста
            icon_offset = 0
            if key == 'delete_1':
                self.scr.blit(self.icon_delete, (text_x + icon_offset, text_y))
                icon_offset += self.icon_size + 4
            elif key == 'delete_9':
                self.scr.blit(self.icon_delete, (text_x + icon_offset, text_y))
                icon_offset += self.icon_size + 4
                self.scr.blit(self.icon_plus, (text_x + icon_offset, text_y))
                icon_offset += self.icon_size + 4
                self.scr.blit(self.icon_radar, (text_x + icon_offset, text_y))
                icon_offset += self.icon_size + 4
            else:  # reset
                self.scr.blit(self.icon_harddisk, (text_x + icon_offset, text_y))
                icon_offset += self.icon_size + 4
            
            # Рисуем текст названия
            self.scr.blit(name_text, (text_x + icon_offset, text_y))
            
            # Прогресс-бар
            bar_x = text_x
            bar_y = y_offset + 35
            
            # Фон бара (тёмно-серый)
            pg.draw.rect(self.scr, (40, 40, 40), (bar_x, bar_y, self.bar_width, self.bar_height))
            pg.draw.rect(self.scr, (80, 80, 80), (bar_x, bar_y, self.bar_width, self.bar_height), 1)
            
            # Цвет бара зависит от процента заполнения
            if ability['cost'] > 0:
                percentage = (self.battlefield.mission_points / ability['cost']) * 100
            else:
                percentage = 100
            
            # Определяем цвет бара по проценту
            if percentage < 30:
                fill_color = (200, 0, 0)      # Красный
            elif percentage < 70:
                fill_color = (255, 165, 0)    # Оранжевый
            else:
                fill_color = (0, 200, 0)      # Зелёный
            
            # Заполнение бара (ограничено 100%)
            fill_ratio = min(percentage / 100, 1.0)
            fill_width = int(self.bar_width * fill_ratio)
            
            if fill_width > 0:
                pg.draw.rect(self.scr, fill_color, (bar_x, bar_y, fill_width, self.bar_height))
            
            # Рамка для активной способности
            if is_active:
                pg.draw.rect(self.scr, (255, 255, 0), (bar_x - 2, bar_y - 2, self.bar_width + 4, self.bar_height + 4), 2)
            
            # Текст под баром
            if can_afford:
                action_text = self.font_text.render("Использовать", True, (100, 255, 100))
            else:
                action_text = self.font_text.render("Недостаточно", True, (255, 100, 100))
            
            self.scr.blit(action_text, (bar_x, bar_y + 20))
            
            y_offset += self.ability_spacing
    
    def handle_click(self, pos):
        mx, my = pos
        
        if not (self.panel_x <= mx <= self.panel_x + self.panel_width and
                self.panel_y <= my <= self.panel_y + self.panel_height):
            return False
        
        y_offset = self.first_ability_y
        for key, ability in self.abilities.items():
            # Область клика для каждой способности
            click_rect = pg.Rect(self.panel_x + 20, y_offset - 10, self.bar_width, 70)
            if click_rect.collidepoint(mx, my):
                if self.battlefield.mission_points >= ability['cost']:
                    if self.active_ability == key:
                        self.active_ability = None
                    else:
                        self.active_ability = key
                return True
            y_offset += self.ability_spacing
        
        return False

    def get_active_ability(self):
        return self.active_ability

    def get_ability_cost(self, key):
        return self.abilities[key]['cost']

    def consume_ability(self):
        if self.active_ability is None:
            return
        cost = self.abilities[self.active_ability]['cost']
        self.battlefield.mission_points -= cost
        self.active_ability = None

    def cancel_selection(self):
        self.active_ability = None