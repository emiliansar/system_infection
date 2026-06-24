import pygame as pg
from pathlib import Path

class SoundManager:
    """Менеджер звуков игры"""
    
    def __init__(self):
        self.sounds_dir = Path(__file__).parent.parent / 'sounds'
        
        # СНАЧАЛА инициализируем громкость
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        
        # Загрузка звуков
        self.sounds = {}
        self._load_sounds()
        
        # Фоновая музыка
        self.current_music = None
    
    def _load_sounds(self):
        """Загружает все звуки"""
        sound_files = {
            'background': 'background.wav',
            'menu_on_start': 'menu_on_start.wav',  # 👇 Обновлённое имя
            'menu_infinite': 'menu_infinite.wav',
            'menu_button_click': 'menu_button_click.wav',
            'positive_connect': 'positive_connect.wav',
            'negative_connect': 'negative_connect.wav',
        }
        
        for name, filename in sound_files.items():
            try:
                path = self.sounds_dir / filename
                self.sounds[name] = pg.mixer.Sound(str(path))
                self.sounds[name].set_volume(self.sfx_volume)
                print(f"[SOUND] Loaded: {filename}")
            except Exception as e:
                print(f"[SOUND] Failed to load {filename}: {e}")
    
    def play_sfx(self, name):
        """Воспроизводит звуковой эффект"""
        if name in self.sounds:
            self.sounds[name].play()
    
    def play_music(self, name, loops=-1):
        """
        Воспроизводит фоновую музыку
        loops=-1 означает бесконечный цикл
        """
        if name in self.sounds:
            # Если уже играет эта музыка — не перезапускаем
            if self.current_music == name:
                return
            
            # Останавливаем текущую музыку
            pg.mixer.music.stop()
            
            # Получаем имя файла
            filename = self._get_filename(name)
            pg.mixer.music.load(str(self.sounds_dir / filename))
            pg.mixer.music.set_volume(self.music_volume)
            pg.mixer.music.play(loops=loops)
            self.current_music = name
            print(f"[SOUND] Playing music: {name} (loops={loops})")
    
    def _get_filename(self, name):
        """Возвращает имя файла для звука"""
        filenames = {
            'background': 'background.wav',
            'menu_on_start': 'menu_on_start.wav',
            'menu_infinite': 'menu_infinite.wav',
        }
        return filenames.get(name, f"{name}.wav")
    
    def stop_music(self):
        """Останавливает фоновую музыку"""
        pg.mixer.music.stop()
        self.current_music = None
    
    def set_music_volume(self, volume):
        """Устанавливает громкость музыки (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pg.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """Устанавливает громкость эффектов (0.0 - 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def play_positive_connect(self):
        """Звук при столкновении одинаковых юнитов"""
        self.play_sfx('positive_connect')
    
    def play_negative_connect(self):
        """Звук при столкновении разных юнитов"""
        self.play_sfx('negative_connect')
    
    def play_menu_click(self):
        """Звук клика по кнопке в меню"""
        self.play_sfx('menu_button_click')