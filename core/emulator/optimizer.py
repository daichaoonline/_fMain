from dataclasses import dataclass, field
from PyQt6.QtCore import QThread, pyqtSignal
import psutil
import time
from PyQt6.QtWidgets import QLabel

@dataclass
class EmulatorOptimizer(QThread):
    cpuThreshold: float
    ramThreshold: float
    lblStatus: QLabel
    checkInterval: float = 2.0
    _running: bool = field(default=True, init=False)

    check_signal: pyqtSignal = field(default_factory=lambda: pyqtSignal(bool), init=False)

    def run_monitoring(self):
        while self._running:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent

            if cpu_usage > self.cpuThreshold or ram_usage > self.ramThreshold:
                self.lblStatus.setText("Pausing Tasks")
                self.lblStatus.setStyleSheet(
                    "font-weight: bold; font-size: 12px; font-family: Arial;"
                )
                self.check_signal.emit(False)
            elif cpu_usage < (self.cpuThreshold - 10) and ram_usage < (self.ramThreshold - 10):
                self.lblStatus.clear()
                self.check_signal.emit(True)

            time.sleep(self.checkInterval)

    def stop_monitoring(self):
        self._running = False