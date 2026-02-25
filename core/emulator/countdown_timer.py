from dataclasses import dataclass, field
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

@dataclass
class CountdownTimer(QObject):
    interval_ms: int = 1000
    _elapsed_seconds: int = field(default=0, init=False)

    time_updated: pyqtSignal = pyqtSignal(int, int, int)
    started: pyqtSignal = pyqtSignal()
    stopped: pyqtSignal = pyqtSignal()

    def __post_init__(self):
        super().__init__()
        self._timer = QTimer(self)
        self._timer.setInterval(self.interval_ms)
        self._timer.timeout.connect(self._update_time)

    def _update_time(self):
        self._elapsed_seconds += 1
        hours = self._elapsed_seconds // 3600
        minutes = (self._elapsed_seconds % 3600) // 60
        seconds = self._elapsed_seconds % 60
        self.time_updated.emit(hours, minutes, seconds)

    def start_timer(self):
        self._elapsed_seconds = 0
        self._timer.start()
        self.started.emit()

    def stop_timer(self):
        self._timer.stop()
        self.stopped.emit()

    def reset_timer(self):
        self._elapsed_seconds = 0
        self._timer.stop()
        self.stopped.emit()