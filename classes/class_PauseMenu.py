import pygame as pg

class PauseMenu:
    def __init__(self, screen, sound_manager=None):  # 👇 Добавлен sound_manager
        self.scr = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.sound_manager = sound_manager
        
        self.font_title = pg.font.Font(None, 96)
        self.font_description = pg.font.Font(None, 36)
        self.font_button = pg.font.Font(None, 48)
        
        self.button_width = 400
        self.button_height = 80
        self.button_x = (self.width - self.button_width) // 2
        
        self.btn_continue_rect = pg.Rect(
            self.button_x, 
            self.height // 2 + 50, 
            self.button_width, 
            self.button_height
        )
        
        self.btn_menu_rect = pg.Rect(
            self.button_x, 
            self.height // 2 + 180, 
            self.button_width, 
            self.button_height
        )
        
        self.btn_quit_rect = pg.Rect(
            self.button_x, 
            self.height // 2 + 310, 
            self.button_width, 
            self.button_height
        )
    
    def draw(self):
        overlay = pg.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.scr.blit(overlay, (0, 0))
        
        title_text = self.font_title.render("Пауза", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 3))
        self.scr.blit(title_text, title_rect)
        
        desc_text = self.font_description.render(
            "Отдыхать тоже надо...", 
            True, 
            (200, 200, 200)
        )
        desc_rect = desc_text.get_rect(center=(self.width // 2, self.height // 3 + 80))
        self.scr.blit(desc_text, desc_rect)
        
        pg.draw.rect(self.scr, (0, 150, 0), self.btn_continue_rect)
        pg.draw.rect(self.scr, (0, 255, 0), self.btn_continue_rect, 3)
        
        continue_text = self.font_button.render("Продолжить", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=self.btn_continue_rect.center)
        self.scr.blit(continue_text, continue_text_rect)
        
        pg.draw.rect(self.scr, (100, 100, 100), self.btn_menu_rect)
        pg.draw.rect(self.scr, (150, 150, 150), self.btn_menu_rect, 3)
        
        menu_text = self.font_button.render("Главное меню", True, (255, 255, 255))
        menu_text_rect = menu_text.get_rect(center=self.btn_menu_rect.center)
        self.scr.blit(menu_text, menu_text_rect)
        
        pg.draw.rect(self.scr, (150, 0, 0), self.btn_quit_rect)
        pg.draw.rect(self.scr, (255, 0, 0), self.btn_quit_rect, 3)
        
        quit_text = self.font_button.render("Папочка я сдаюсь", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=self.btn_quit_rect.center)
        self.scr.blit(quit_text, quit_text_rect)
    
    def handle_click(self, pos):
        if self.btn_continue_rect.collidepoint(pos):
            if self.sound_manager:
                self.sound_manager.play_menu_click()
            return 'continue'
        elif self.btn_menu_rect.collidepoint(pos):
            if self.sound_manager:
                self.sound_manager.play_menu_click()
            return 'menu'
        elif self.btn_quit_rect.collidepoint(pos):
            if self.sound_manager:
                self.sound_manager.play_menu_click()
            return 'quit'
        return None