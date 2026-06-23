import pygame as pg
import random
import sys

class Overlay:
    """Overlay с глитч-эффектами для отображения при поражении"""
    
    def __init__(self, screen):
        self.scr = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Сообщения для отображения
        self.messages = [
            "CRITICAL ERROR",
            "SYSTEM FAILURE",
            "DATA CORRUPTION",
            "FATAL EXCEPTION 0x0000000",
            "MEMORY LEAK DETECTED",
            "SYSTEM HALTED",
            " unrecoverable ERROR",
            "KERNEL PANIC",
            "BLUE SCREEN OF DEATH"
        ]
        
        self.current_message = ""
        self.message_timer = 0
        self.message_change_interval = 2000  # мс
        
        # Эффекты
        self.glitch_offset = (0, 0)
        self.scanline_offset = 0
        self.brightness = 255
        self.flicker_timer = 0
        
        # Артефакты (горизонтальные линии)
        self.artifacts = []
        self.max_artifacts = 5
        
        # Шрифты
        self.font_large = pg.font.Font(None, 72)
        self.font_medium = pg.font.Font(None, 36)
        
        # Состояние
        self.active = False
        self.alpha = 0
        self.fade_speed = 5
        
        # Часы для timing
        self.clock = pg.time.Clock()
        self.last_time = pg.time.get_ticks()
    
    def start(self):
        """Активировать overlay"""
        self.active = True
        self.current_message = random.choice(self.messages)
        self.alpha = 0
        self._generate_artifacts()
    
    def stop(self):
        """Деактивировать overlay"""
        self.active = False
    
    def _generate_artifacts(self):
        """Сгенерировать случайные артефакты"""
        self.artifacts = []
        for _ in range(self.max_artifacts):
            y = random.randint(0, self.height)
            height = random.randint(2, 10)
            width = random.randint(100, self.width)
            x = random.randint(0, self.width - width)
            alpha = random.randint(50, 150)
            self.artifacts.append([x, y, width, height, alpha])
    
    def _update_effects(self, dt):
        """Обновить эффекты"""
        current_time = pg.time.get_ticks()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Обновление сообщения
        self.message_timer += dt
        if self.message_timer >= self.message_change_interval:
            self.message_timer = 0
            self.current_message = random.choice(self.messages)
        
        # Глитч-смещение
        if random.random() < 0.1:
            self.glitch_offset = (
                random.randint(-10, 10),
                random.randint(-5, 5)
            )
        else:
            self.glitch_offset = (
                self.glitch_offset[0] * 0.9,
                self.glitch_offset[1] * 0.9
            )
        
        # Мерцание
        self.flicker_timer += dt
        if self.flicker_timer > 100:
            self.flicker_timer = 0
            if random.random() < 0.2:
                self.brightness = random.randint(200, 255)
            else:
                self.brightness = 255
        
        # Обновление артефактов
        if random.random() < 0.05:
            self._generate_artifacts()
        
        for artifact in self.artifacts:
            artifact[1] += 2  # Движение вниз
            artifact[4] -= 1  # Уменьшение прозрачности
        
        # Удаление исчезнувших артефактов
        self.artifacts = [a for a in self.artifacts if a[4] > 0 and a[1] < self.height]
        
        # Добавление новых артефактов
        if len(self.artifacts) < self.max_artifacts and random.random() < 0.1:
            y = 0
            height = random.randint(2, 8)
            width = random.randint(50, 300)
            x = random.randint(0, self.width - width)
            alpha = random.randint(80, 180)
            self.artifacts.append([x, y, width, height, alpha])
        
        # Пульсация
        self.scanline_offset = (self.scanline_offset + 1) % 10
        
        # Fade in
        if self.alpha < 200:
            self.alpha += self.fade_speed
    
    def draw(self):
        """Отрисовать overlay"""
        if not self.active:
            return
        
        # Полупрозрачный фон
        overlay = pg.Surface((self.width, self.height))
        overlay.set_alpha(self.alpha)
        overlay.fill((0, 0, 0))
        self.scr.blit(overlay, (0, 0))
        
        # Артефакты (горизонтальные линии)
        for artifact in self.artifacts:
            x, y, w, h, alpha = artifact
            color = (random.randint(0, 100), random.randint(150, 255), random.randint(0, 100))
            artifact_surface = pg.Surface((w, h))
            artifact_surface.set_alpha(alpha * (self.alpha / 200))
            artifact_surface.fill(color)
            self.scr.blit(artifact_surface, (x, y))
        
        # Сканирующие линии
        for y in range(0, self.height, 4):
            alpha = 30 if (y + self.scanline_offset) % 8 < 4 else 10
            line_surface = pg.Surface((self.width, 2))
            line_surface.set_alpha(alpha * (self.alpha / 200))
            line_surface.fill((0, 255, 0))
            self.scr.blit(line_surface, (0, y))
        
        # Основное сообщение с глитч-эффектом
        if self.current_message:
            # RGB split эффект
            text_surface_r = self.font_large.render(self.current_message, True, (255, 0, 0))
            text_surface_g = self.font_large.render(self.current_message, True, (0, 255, 0))
            text_surface_b = self.font_large.render(self.current_message, True, (0, 0, 255))
            
            # Смещения для каждого канала
            offset_x, offset_y = self.glitch_offset
            
            # Отрисовка с наложением
            self.scr.blit(text_surface_r, (
                self.width // 2 - text_surface_r.get_width() // 2 + offset_x,
                self.height // 2 - 50 + offset_y
            ))
            self.scr.blit(text_surface_g, (
                self.width // 2 - text_surface_g.get_width() // 2,
                self.height // 2 - 50
            ))
            self.scr.blit(text_surface_b, (
                self.width // 2 - text_surface_b.get_width() // 2 - offset_x,
                self.height // 2 - 50 - offset_y
            ))
            
            # Белое основное сообщение
            text_surface = self.font_large.render(self.current_message, True, (255, 255, 255))
            self.scr.blit(text_surface, (
                self.width // 2 - text_surface.get_width() // 2,
                self.height // 2 - 50
            ))
        
        # Дополнительный текст
        sub_text = self.font_medium.render("SYSTEM COMPROMISED", True, (255, 100, 100))
        self.scr.blit(sub_text, (
            self.width // 2 - sub_text.get_width() // 2,
            self.height // 2 + 50
        ))
        
        # Виньетка (затемнение по краям)
        vignette = pg.Surface((self.width, self.height))
        vignette.set_alpha(100 * (self.alpha / 200))
        vignette.fill((0, 0, 0))
        # Вырезаем центр
        center_surface = pg.Surface((self.width // 2, self.height // 2))
        center_surface.fill((0, 0, 0))
        vignette.blit(center_surface, (self.width // 4, self.height // 4), special_flags=pg.BLEND_RGBA_SUB)
        self.scr.blit(vignette, (0, 0))