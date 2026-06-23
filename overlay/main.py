#!/usr/bin/env python3
import pygame as pg
import sys
import os
import random
import time
from pathlib import Path

# Инициализация pygame
pg.init()

# Получаем путь к файлу статуса
OVERLAY_DIR = Path(__file__).parent.resolve()
STATUS_FILE = OVERLAY_DIR / 'status.txt'

print(f"[OVERLAY] Starting...")
print(f"[OVERLAY] Overlay directory: {OVERLAY_DIR}")
print(f"[OVERLAY] Status file: {STATUS_FILE}")
print(f"[OVERLAY] Status file exists: {STATUS_FILE.exists()}")

# Проверяем начальный статус
initial_status = 'normal'
if STATUS_FILE.exists():
    try:
        initial_status = STATUS_FILE.read_text(encoding='utf-8').strip().lower()
        print(f"[OVERLAY] Initial status: {initial_status}")
    except Exception as e:
        print(f"[OVERLAY] Error reading status: {e}")

# Настройки экрана
info = pg.display.Info()
screen = pg.display.set_mode((info.current_w, info.current_h), pg.FULLSCREEN)
pg.display.set_caption("System Overlay")
clock = pg.time.Clock()

# Скрываем курсор
pg.mouse.set_visible(False)

# Шрифты
font_large = pg.font.Font(None, 96)
font_medium = pg.font.Font(None, 48)

# Сообщения для разных состояний
STATE_MESSAGES = {
    'normal': [],
    'critical': [
        'CRITICAL ERROR',
        'SYSTEM FAILURE',
        'FATAL EXCEPTION',
        'DATA CORRUPTION',
        'KERNEL PANIC',
        'SYSTEM HALTED',
        'UNRECOVERABLE ERROR'
    ]
}

def read_status():
    """Читает статус из файла"""
    try:
        if STATUS_FILE.exists():
            status = STATUS_FILE.read_text(encoding='utf-8').strip().lower()
            if status in ['normal', 'critical']:
                return status
    except Exception as e:
        print(f"[OVERLAY] Error reading status: {e}")
    return 'normal'

def main():
    current_state = initial_status
    current_message = ""
    message_timer = 0
    alpha = 0
    target_alpha = 200 if current_state == 'critical' else 0
    
    # Эффекты
    glitch_offset = (0, 0)
    artifacts = []
    scanline_y = 0
    brightness = 255
    
    print(f"[OVERLAY] Main loop started, state: {current_state}")
    
    running = True
    frame_count = 0
    
    while running:
        dt = clock.tick(60)
        frame_count += 1
        
        # Печатаем статус каждые 100 кадров
        if frame_count % 100 == 0:
            print(f"[OVERLAY] Frame {frame_count}, state: {current_state}, alpha: {alpha}")
        
        # Чтение статуса
        new_state = read_status()
        if new_state != current_state:
            print(f"[OVERLAY] State changed: {current_state} -> {new_state}")
            current_state = new_state
            current_message = ""
            message_timer = 0
            if new_state == 'critical':
                target_alpha = 200
            else:
                target_alpha = 0
        
        # Fade in/out
        diff = target_alpha - alpha
        alpha += diff * 0.05
        
        # Если полностью прозрачный и статус normal — выходим
        if alpha < 1 and current_state == 'normal':
            print(f"[OVERLAY] Exiting, frame_count: {frame_count}")
            break
        
        # Обработка событий
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("[OVERLAY] QUIT event received")
                running = False
            
            if event.type == pg.KEYDOWN:
                print(f"[OVERLAY] Key pressed: {event.key}")
                # Закрытие overlay по R, ESC, Space, Enter или любой клавише
                if event.key in [pg.K_r, pg.K_ESCAPE, pg.K_SPACE, pg.K_RETURN]:
                    print("[OVERLAY] Closing overlay by key press")
                    STATUS_FILE.write_text('normal', encoding='utf-8')
                    running = False
        
        # Обновление эффектов
        if alpha > 1:
            # Глитч смещение
            if random.random() < 0.15:
                glitch_offset = (random.randint(-15, 15), random.randint(-8, 8))
            else:
                glitch_offset = (int(glitch_offset[0] * 0.9), int(glitch_offset[1] * 0.9))
            
            # Мерцание
            if random.random() < 0.1:
                brightness = random.randint(150, 255)
            else:
                brightness = min(255, brightness + 10)
            
            # Артефакты
            if random.random() < 0.1:
                y = random.randint(0, screen.get_height())
                height = random.randint(2, 15)
                width = random.randint(100, screen.get_width())
                x = random.randint(0, screen.get_width() - width)
                color = (random.randint(0, 100), random.randint(150, 255), random.randint(0, 100))
                alpha_art = random.randint(50, 150)
                artifacts.append([x, y, width, height, color, alpha_art])
            
            # Движение артефактов
            for artifact in artifacts:
                artifact[1] += 3
                artifact[5] -= 2
            
            artifacts = [a for a in artifacts if a[5] > 0 and a[1] < screen.get_height()]
            
            # Сканирующие линии
            scanline_y = (scanline_y + 2) % 10
            
            # Обновление сообщения
            message_timer += 1
            if message_timer > 120:
                message_timer = 0
                messages = STATE_MESSAGES.get(current_state, [])
                if messages:
                    current_message = random.choice(messages)
        
        # Отрисовка
        screen.fill((0, 0, 0))
        
        if alpha > 1:
            # Полупрозрачный фон
            overlay = pg.Surface(screen.get_size())
            overlay.set_alpha(int(alpha))
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Артефакты
            for artifact in artifacts:
                x, y, w, h, color, alpha_art = artifact
                artifact_surface = pg.Surface((w, h))
                artifact_surface.set_alpha(int(alpha_art * (alpha / 200)))
                artifact_surface.fill(color)
                screen.blit(artifact_surface, (x, y))
            
            # Сканирующие линии
            for y in range(0, screen.get_height(), 4):
                line_alpha = 40 if (y + scanline_y) % 8 < 4 else 15
                line_surface = pg.Surface((screen.get_width(), 2))
                line_surface.set_alpha(int(line_alpha * (alpha / 200)))
                line_surface.fill((0, 255, 0))
                screen.blit(line_surface, (0, y))
            
            # Текст с глитч-эффектом
            if current_message and current_state == 'critical':
                # RGB split эффект
                text_r = font_large.render(current_message, True, (255, 0, 0))
                text_g = font_large.render(current_message, True, (0, 255, 0))
                text_b = font_large.render(current_message, True, (0, 0, 255))
                
                offset_x, offset_y = glitch_offset
                center_x = screen.get_width() // 2
                center_y = screen.get_height() // 2 - 50
                
                # Отрисовка каналов с смещением
                screen.blit(text_r, (center_x - text_r.get_width() // 2 + offset_x, 
                                     center_y + offset_y))
                screen.blit(text_g, (center_x - text_g.get_width() // 2, center_y))
                screen.blit(text_b, (center_x - text_b.get_width() // 2 - offset_x, 
                                     center_y - offset_y))
                
                # Белый текст поверх
                text_white = font_large.render(current_message, True, (255, 255, 255))
                screen.blit(text_white, (center_x - text_white.get_width() // 2, center_y))
                
                # Дополнительный текст
                sub_text = font_medium.render("SYSTEM COMPROMISED", True, (255, 100, 100))
                screen.blit(sub_text, (center_x - sub_text.get_width() // 2, center_y + 80))
        
        pg.display.flip()
    
    # Восстанавливаем курсор
    pg.mouse.set_visible(True)
    print("[OVERLAY] Quitting...")
    pg.quit()
    sys.exit()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[OVERLAY] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        pg.quit()
        sys.exit(1)