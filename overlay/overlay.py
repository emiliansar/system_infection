import sys
import random
from PyQt6.QtCore import Qt, QTimer, QPoint, pyqtSignal, QSize, QPointF
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QScreen

from effects import GlitchEffects, AnimationController
from reader import StatusReader


class OverlayWindow(QWidget):
    toggle_signal = pyqtSignal(bool)
    close_signal = pyqtSignal()

    STATE_MESSAGES = {
        'normal': [],
        'critical': [
            'CRITICAL ERROR',
            'SYSTEM CRASH IMMINENT',
            'FATAL EXCEPTION',
            'DATA CORRUPTION',
            'EMERGENCY SHUTDOWN',
            '!!! WARNING !!!',
            'KERNEL PANIC',
            'SYSTEM HALTED',
        ],
    }

    def __init__(self):
        super().__init__()
        self._setup_window()
        self.activateWindow()
        self.setFocus()
        
        self._effects = GlitchEffects(intensity=0.5)
        self._animation = AnimationController()
        self._reader = StatusReader()
        
        self._current_state = 'normal'
        self._is_active = True
        self._enabled = True
        self._messages = []
        self._current_message = ''
        self._message_timer = 0
        
        self._effects_timer = QTimer()
        self._effects_timer.timeout.connect(self._update_effects)
        self._effects_timer.start(50)
        
        self._status_timer = QTimer()
        self._status_timer.timeout.connect(self._check_status)
        self._status_timer.start(100)
        
        self._update_messages()
        self._apply_state('normal')

    def _setup_window(self):
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.geometry()
            self.setGeometry(geometry)
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _update_effects(self):
        self._effects.update(50)
        self._animation.update(50)
        self._message_timer += 50
        if self._message_timer > 2000:
            self._message_timer = 0
            self._rotate_message()
        if random.random() < 0.005:
            self._effects.trigger_burst()
        self.update()

    def _check_status(self):
        new_state = self._reader.get_current_state()
        if new_state != self._current_state:
            self._apply_state(new_state)
            self._current_state = new_state
        
        if new_state == 'normal':
            if self._animation.is_visible:
                self._animation.fade_out(0.1)
        else:
            if not self._animation.is_visible:
                self._animation.fade_in(0.1)

    def _apply_state(self, state):
        self._current_state = state
        self._update_messages()
        if state == 'critical':
            self._effects.set_intensity(1.0)
            self._animation.enable_pulse(amplitude=0.2, frequency=3.0)
        else:
            self._effects.set_intensity(0.0)
            self._animation.disable_pulse()

    def _update_messages(self):
        self._messages = self.STATE_MESSAGES.get(self._current_state, [])
        self._current_message = random.choice(self._messages) if self._messages else ''

    def _rotate_message(self):
        if self._messages:
            self._current_message = random.choice(self._messages)

    def paintEvent(self, event):
        if not self._enabled:
            return
        opacity = self._animation.get_current_opacity() * self._effects.opacity
        if opacity < 0.05:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._draw_artifacts(painter, opacity)
        self._draw_glitch_text(painter, opacity)
        if self._effects.burst_active:
            self._draw_burst(painter, opacity)
        painter.end()

    def _draw_artifacts(self, painter, base_opacity):
        for y, height, width, alpha in self._effects.artifacts:
            x = random.randint(0, self.width() - width)
            color = QColor(0, 255, 65, int(alpha * base_opacity))
            painter.fillRect(x, y, width, height, color)

    def _draw_glitch_text(self, painter, base_opacity):
        if not self._current_message:
            return
        jitter_x, jitter_y = self._effects.jitter_offset
        center_x = self.width() // 2 + jitter_x
        center_y = self.height() // 2 + jitter_y
        font = QFont('Consolas', 48, QFont.Weight.Bold)
        painter.setFont(font)
        rgb_offsets = self._effects.rgb_offsets
        flicker = self._effects.flicker_alpha
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for i, (r, g, b) in enumerate(colors):
            offset_x, offset_y = rgb_offsets[i]
            alpha = int(flicker * base_opacity)
            color = QColor(r, g, b, alpha)
            painter.setPen(QPen(color))
            painter.drawText(
                QPointF(center_x + offset_x - 200, center_y + offset_y),
                self._current_message
            )
        white_alpha = int(200 * base_opacity)
        painter.setPen(QPen(QColor(255, 255, 255, white_alpha)))
        painter.drawText(QPointF(center_x - 200, center_y), self._current_message)

    def _draw_burst(self, painter, base_opacity):
        color = QColor(255, 255, 255, int(100 * base_opacity))
        painter.fillRect(self.rect(), color)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F10:
            self.toggle()
        elif event.key() == Qt.Key.Key_Escape:
            self.close_overlay()

    def toggle(self):
        self._enabled = not self._enabled
        if self._enabled:
            self.show()
        else:
            self.hide()
        self.toggle_signal.emit(self._enabled)

    def close_overlay(self):
        self.close_signal.emit()
        self.close()
        QApplication.quit()

    def set_enabled(self, enabled):
        self._enabled = enabled

    @property
    def is_enabled(self):
        return self._enabled


class OverlayApp:
    def __init__(self):
        self.app = None
        self.overlay = None

    def run(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName('GameOverlay')
        self.overlay = OverlayWindow()
        self.overlay.show()
        return self.app.exec()

    def get_overlay(self):
        return self.overlay