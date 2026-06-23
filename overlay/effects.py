import random
import math

class GlitchEffects:
    def __init__(self, intensity=0.5):
        self.intensity = intensity
        self._random = random.Random()
        self._random.seed()
        self._time = 0
        self._jitter_offset = (0, 0)
        self._rgb_offsets = [(0, 0), (0, 0), (0, 0)]
        self._flicker_alpha = 255
        self._artifacts = []
        self._burst_active = False
        self._burst_timer = 0
        self._visible = True
        self._opacity = 1.0

    def update(self, delta_ms=50):
        self._time += delta_ms
        self._update_jitter()
        self._update_rgb_split()
        self._update_flicker()
        self._update_artifacts()
        self._update_burst(delta_ms)
        self._update_opacity()

    def _update_jitter(self):
        if self._random.random() < 0.3 * self.intensity:
            self._jitter_offset = (
                self._random.randint(-5, 5) * self.intensity,
                self._random.randint(-3, 3) * self.intensity
            )
        else:
            self._jitter_offset = (0, 0)

    def _update_rgb_split(self):
        if self._random.random() < 0.2 * self.intensity:
            offset_range = int(8 * self.intensity)
            self._rgb_offsets = [
                (self._random.randint(-offset_range, offset_range),
                 self._random.randint(-offset_range, offset_range))
                for _ in range(3)
            ]
        else:
            self._rgb_offsets = [(int(x * 0.9), int(y * 0.9)) for x, y in self._rgb_offsets]

    def _update_flicker(self):
        if self._random.random() < 0.15 * self.intensity:
            self._flicker_alpha = self._random.randint(100, 255)
        else:
            self._flicker_alpha = min(255, self._flicker_alpha + 5)

    def _update_artifacts(self):
        if self._random.random() < 0.25 * self.intensity:
            y = self._random.randint(0, 800)
            height = self._random.randint(2, 20)
            width = self._random.randint(50, 400)
            self._artifacts.append((y, height, width, self._random.randint(50, 200)))
        if len(self._artifacts) > 10:
            self._artifacts.pop(0)
        self._artifacts = [(y, h, w, a - 5) for y, h, w, a in self._artifacts if a > 0]

    def _update_burst(self, delta_ms):
        if self._burst_active:
            self._burst_timer -= delta_ms
            if self._burst_timer <= 0:
                self._burst_active = False
        elif self._random.random() < 0.02 * self.intensity:
            self.trigger_burst()

    def _update_opacity(self):
        if self._random.random() < 0.1:
            if self._visible:
                target = self._random.uniform(0.7, 1.0)
            else:
                target = 0.0
            self._opacity += (target - self._opacity) * 0.1

    @property
    def jitter_offset(self): return self._jitter_offset

    @property
    def rgb_offsets(self): return self._rgb_offsets

    @property
    def flicker_alpha(self): return self._flicker_alpha

    @property
    def artifacts(self): return self._artifacts

    @property
    def opacity(self): return self._opacity

    @property
    def burst_active(self): return self._burst_active

    def trigger_burst(self):
        self._burst_active = True
        self._burst_timer = 200
        self._flicker_alpha = 255

    def set_intensity(self, value):
        self.intensity = max(0.0, min(1.0, value))

    def set_visible(self, visible):
        self._visible = visible


class AnimationController:
    def __init__(self):
        self._fade_progress = 0.0
        self._target_opacity = 0.0
        self._fade_speed = 0.05
        self._pulse_enabled = False
        self._pulse_phase = 0.0
        self._pulse_amplitude = 0.1
        self._pulse_frequency = 2.0

    def update(self, delta_ms=50):
        diff = self._target_opacity - self._fade_progress
        self._fade_progress += diff * self._fade_speed
        if self._pulse_enabled:
            self._pulse_phase += delta_ms / 1000.0 * self._pulse_frequency

    def get_current_opacity(self):
        base = self._fade_progress
        if self._pulse_enabled:
            pulse = math.sin(self._pulse_phase) * self._pulse_amplitude
            return max(0.0, min(1.0, base + pulse))
        return base

    def fade_in(self, speed=0.05):
        self._target_opacity = 1.0
        self._fade_speed = speed

    def fade_out(self, speed=0.05):
        self._target_opacity = 0.0
        self._fade_speed = speed

    def enable_pulse(self, amplitude=0.1, frequency=2.0):
        self._pulse_enabled = True
        self._pulse_amplitude = amplitude
        self._pulse_frequency = frequency

    def disable_pulse(self):
        self._pulse_enabled = False

    @property
    def is_fading_in(self): return self._target_opacity > self._fade_progress

    @property
    def is_fading_out(self): return self._target_opacity < self._fade_progress

    @property
    def is_visible(self): return self._fade_progress > 0.1