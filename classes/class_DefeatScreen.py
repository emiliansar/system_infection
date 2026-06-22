import pygame as pg

class DefeatScreen:
    def __init__(self, screen):
        self.scr = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.font_title = pg.font.Font(None, 72)
        self.font_description = pg.font.Font(None, 36)
        self.font_button = pg.font.Font(None, 48)
        
        # Размер кнопок
        self.button_width = 400
        self.button_height = 80
        self.button_x = (self.width - self.button_width) // 2
        
        # Кнопка "Играть заново"
        self.btn_restart_rect = pg.Rect(
            self.button_x, 
            self.height // 2 + 100, 
            self.button_width, 
            self.button_height
        )
        
        # Кнопка "Главное меню"
        self.btn_menu_rect = pg.Rect(
            self.button_x, 
            self.height // 2 + 220, 
            self.button_width, 
            self.button_height
        )
    
    def draw(self):
        # Полупрозрачный чёрный фон
        overlay = pg.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.scr.blit(overlay, (0, 0))
        
        # Заголовок
        title_text = self.font_title.render("Поражение", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.scr.blit(title_text, title_rect)
        
        # Описание
        desc_text = self.font_description.render(
            "Вирусы захватили ваш компьютер", 
            True, 
            (200, 200, 200)
        )
        desc_rect = desc_text.get_rect(center=(self.width // 2, self.height // 2 - 30))
        self.scr.blit(desc_text, desc_rect)
        
        # Кнопка "Играть заново"
        pg.draw.rect(self.scr, (0, 150, 0), self.btn_restart_rect)
        pg.draw.rect(self.scr, (0, 255, 0), self.btn_restart_rect, 3)
        
        restart_text = self.font_button.render("Играть заново", True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=self.btn_restart_rect.center)
        self.scr.blit(restart_text, restart_text_rect)
        
        # Кнопка "Главное меню"
        pg.draw.rect(self.scr, (100, 100, 100), self.btn_menu_rect)
        pg.draw.rect(self.scr, (150, 150, 150), self.btn_menu_rect, 3)
        
        menu_text = self.font_button.render("Главное меню", True, (255, 255, 255))
        menu_text_rect = menu_text.get_rect(center=self.btn_menu_rect.center)
        self.scr.blit(menu_text, menu_text_rect)
    
    def handle_click(self, pos):
        """
        Обрабатывает клик по экрану поражения.
        Возвращает:
        - 'restart' если клик по кнопке "Играть заново"
        - 'menu' если клик по кнопке "Главное меню"
        - None если клик не попал по кнопкам
        """
        if self.btn_restart_rect.collidepoint(pos):
            return 'restart'
        elif self.btn_menu_rect.collidepoint(pos):
            return 'menu'
        return None