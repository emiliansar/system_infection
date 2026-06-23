#!/usr/bin/env python3
import random
import math

class GlitchEffect:
    """Класс для управления глитч-эффектами"""
    
    def __init__(self, intensity=0.7):
        self.intensity = intensity
        self.offset_x = 0
        self.offset_y = 0
        self.rgb_offsets = [(0, 0), (0, 0), (0, 0)]
        self.flicker_alpha = 255
        self.artifacts = []
        self.scanline_offset = 0
        self.burst_active = False
        self.burst_timer = 0
        self.opacity = 1.0
        self.visible = True
        
    def update(self, dt=16):
        """Обновление эффектов"""
        self._update_jitter()
        self._update_rgb_split()
        self._update_flicker()
        self._update_artifacts()
        self._update_scanlines()
        self._update_burst(dt)
        self._update_opacity()
    
    def _update_jitter(self):
        """Обновление случайного смещения"""
        if random.random() < 0.2 * self.intensity:
            self.offset_x = random.randint(-15, 15) * self.intensity
            self.offset_y = random.randint(-8, 8) * self.intensity
        else:
            self.offset_x *= 0.9
            self.offset_y *= 0.9
    
    def _update_rgb_split(self):
        """Обновление разделения RGB каналов"""
        if random.random() < 0.15 * self.intensity:
            offset_range = int(10 * self.intensity)
            self.rgb_offsets = [
                (random.randint(-offset_range, offset_range),
                 random.randint(-offset_range, offset_range))
                for _ in range(3)
            ]
        else:
            self.rgb_offsets = [
                (int(x * 0.9), int(y * 0.9)) 
                for x, y in self.rgb_offsets
            ]
    
    def _update_flicker(self):
        """Обновление мерцания"""
        if random.random() < 0.1 * self.intensity:
            self.flicker_alpha = random.randint(150, 255)
        else:
            self.flicker_alpha = min(255, self.flicker_alpha + 8)
    
    def _update_artifacts(self):
        """Обновление артефактов (горизонтальных линий)"""
        # Добавление новых артефактов
        if random.random() < 0.2 * self.intensity:
            y = random.randint(0, 800)
            height = random.randint(2, 15)
            width = random.randint(100, 600)
            x = random.randint(0, 1920 - width)
            alpha = random.randint(50, 180)
            color = (
                random.randint(0, 100),
                random.randint(150, 255),
                random.randint(0, 100)
            )
            self.artifacts.append([x, y, width, height, color, alpha])
        
        # Движение и удаление артефактов
        for artifact in self.artifacts:
            artifact[1] += 3  # Движение вниз
            artifact[5] -= 1.5  # Уменьшение прозрачности
        
        # Удаление исчезнувших артефактов
        self.artifacts = [
            a for a in self.artifacts 
            if a[5] > 0 and a[1] < 1080
        ]
        
        # Ограничение количества
        if len(self.artifacts) > 8:
            self.artifacts = self.artifacts[-8:]
    
    def _update_scanlines(self):
        """Обновление сканирующих линий"""
        self.scanline_offset = (self.scanline_offset + 2) % 10
    
    def _update_burst(self, dt):
        """Обновление вспышек"""
        if self.burst_active:
            self.burst_timer -= dt
            if self.burst_timer <= 0:
                self.burst_active = False
        elif random.random() < 0.01 * self.intensity:
            self.trigger_burst()
    
    def _update_opacity(self):
        """Обновление общей прозрачности"""
        if random.random() < 0.05:
            if self.visible:
                target = random.uniform(0.8, 1.0)
            else:
                target = 0.0
            self.opacity += (target - self.opacity) * 0.1
    
    def trigger_burst(self):
        """Триггер вспышки"""
        self.burst_active = True
        self.burst_timer = 150
        self.flicker_alpha = 255
    
    def set_intensity(self, value):
        """Установка интенсивности эффектов (0.0 - 1.0)"""
        self.intensity = max(0.0, min(1.0, value))
    
    def set_visible(self, visible):
        """Установка видимости"""
        self.visible = visible
    
    @property
    def jitter_offset(self):
        """Получить смещение джиттера"""
        return (int(self.offset_x), int(self.offset_y))
    
    @property
    def rgb_offsets(self):
        """Получить смещения RGB каналов"""
        return self.rgb_offsets
    
    @property
    def flicker_alpha(self):
        """Получить альфа-канал мерцания"""
        return self.flicker_alpha
    
    @property
    def artifacts(self):
        """Получить список артефактов"""
        return self.artifacts
    
    @property
    def scanline_y(self):
        """Получить позицию сканирующей линии"""
        return self.scanline_offset
    
    @property
    def burst_active(self):
        """Проверка активности вспышки"""
        return self.burst_active
    
    @property
    def opacity(self):
        """Получить общую прозрачность"""
        return self.opacity


class AnimationController:
    """Контроллер анимаций (fade in/out, пульсация)"""
    
    def __init__(self):
        self.fade_progress = 0.0
        self.target_opacity = 0.0
        self.fade_speed = 0.05
        self.pulse_enabled = False
        self.pulse_phase = 0.0
        self.pulse_amplitude = 0.1
        self.pulse_frequency = 2.0
    
    def update(self, dt=16):
        """Обновление анимаций"""
        # Fade эффект
        diff = self.target_opacity - self.fade_progress
        self.fade_progress += diff * self.fade_speed
        
        # Пульсация
        if self.pulse_enabled:
            self.pulse_phase += dt / 1000.0 * self.pulse_frequency
    
    def get_current_opacity(self):
        """Получить текущую прозрачность"""
        base = self.fade_progress
        if self.pulse_enabled:
            pulse = math.sin(self.pulse_phase) * self.pulse_amplitude
            return max(0.0, min(1.0, base + pulse))
        return base
    
    def fade_in(self, speed=0.05):
        """Анимация появления"""
        self.target_opacity = 1.0
        self.fade_speed = speed
    
    def fade_out(self, speed=0.05):
        """Анимация исчезновения"""
        self.target_opacity = 0.0
        self.fade_speed = speed
    
    def enable_pulse(self, amplitude=0.1, frequency=2.0):
        """Включить пульсацию"""
        self.pulse_enabled = True
        self.pulse_amplitude = amplitude
        self.pulse_frequency = frequency
    
    def disable_pulse(self):
        """Выключить пульсацию"""
        self.pulse_enabled = False
    
    @property
    def is_fading_in(self):
        """Проверка fading in"""
        return self.target_opacity > self.fade_progress
    
    @property
    def is_fading_out(self):
        """Проверка fading out"""
        return self.target_opacity < self.fade_progress
    
    @property
    def is_visible(self):
        """Проверка видимости"""
        return self.fade_progress > 0.1