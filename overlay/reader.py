#!/usr/bin/env python3
from pathlib import Path
from typing import Optional

class StatusReader:
    STATUS_FILE = 'status.txt'
    STATE_NORMAL = 'normal'
    STATE_CRITICAL = 'critical'
    VALID_STATES = [STATE_NORMAL, STATE_CRITICAL]

    def __init__(self):
        self._last_content = None
        self._current_state = self.STATE_NORMAL
        self._file_path = self._get_status_file_path()

    def _get_status_file_path(self):
        return Path(__file__).parent.resolve() / self.STATUS_FILE

    def get_current_state(self):
        try:
            if not self._file_path.exists():
                return self.STATE_NORMAL
            c = self._file_path.read_text(encoding='utf-8').strip().lower()
            if c in self.VALID_STATES:
                self._current_state = c
                self._last_content = c
            else:
                self._current_state = self.STATE_NORMAL
        except:
            self._current_state = self.STATE_NORMAL
        return self._current_state

    def has_changed(self):
        return self.get_current_state() != self._last_content

    @property
    def state(self): return self._current_state

    @property
    def is_active(self): return self._current_state != self.STATE_NORMAL

    @property
    def is_critical(self): return self._current_state == self.STATE_CRITICAL

    @property
    def file_path(self): return str(self._file_path)