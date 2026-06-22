import pygame as pg

class MainMenu:
    def __init__(self, screen):
        self.scr = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.font_title = pg.font.Font(None, 96)
        self.font_description = pg.font.Font(None, 36)
        self.font_button = pg.font.Font(None, 48)
        
        # Кнопки
        self.button_width = 400
        self.button_height = 80
        self.button_x = (self.width - self.button_width) // 2
        
        self.btn_play_rect = pg.Rect(
            self.button_x, 
            self.height // 2 + 50, 
            self.button_width, 
            self.button_height
        )
        
        self.btn_quit_rect = pg.Rect(
            self.button_x, 
            self.height // 2 + 180, 
            self.button_width, 
            self.button_height
        )
    
    def draw(self):
        # Фон
        self.scr.fill((20, 20, 20))
        
        # Заголовок
        title_text = self.font_title.render("Заражение системы", True, (0, 255, 0))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 3))
        self.scr.blit(title_text, title_rect)
        
        # Описание
        desc_text = self.font_description.render(
            "Не дайте вирусам захватить ваш компьютер", 
            True, 
            (200, 200, 200)
        )
        desc_rect = desc_text.get_rect(center=(self.width // 2, self.height // 3 + 80))
        self.scr.blit(desc_text, desc_rect)
        
        # Кнопка "Играть"
        pg.draw.rect(self.scr, (0, 150, 0), self.btn_play_rect)
        pg.draw.rect(self.scr, (0, 255, 0), self.btn_play_rect, 3)
        
        play_text = self.font_button.render("Играть", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=self.btn_play_rect.center)
        self.scr.blit(play_text, play_text_rect)
        
        # Кнопка "Я сдаюсь папочка"
        pg.draw.rect(self.scr, (150, 0, 0), self.btn_quit_rect)
        pg.draw.rect(self.scr, (255, 0, 0), self.btn_quit_rect, 3)
        
        quit_text = self.font_button.render("Я сдаюсь папочка", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=self.btn_quit_rect.center)
        self.scr.blit(quit_text, quit_text_rect)
    
    def handle_click(self, pos):
        """
        Обрабатывает клик по меню.
        Возвращает:
        - 'play' если клик по кнопке "Играть"
        - 'quit' если клик по кнопке "Я сдаюсь папочка"
        - None если клик не попал по кнопкам
        """
        if self.btn_play_rect.collidepoint(pos):
            return 'play'
        elif self.btn_quit_rect.collidepoint(pos):
            return 'quit'
        return None