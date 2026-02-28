from PyQt6.QtCore import QThread, pyqtSignal
from thw_emulator import EmulatorManager

class EmulatorPopulator(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(int)
    error_signal = pyqtSignal(str)
    emulator_signal = pyqtSignal(dict)

    def __init__(self, ld_dir: str):
        super().__init__()
        self.ld_dir = ld_dir

    def run(self):
        try:
            emulator = EmulatorManager(self.ld_dir)
            total = len(emulator.ldplayer)

            if total == 0:
                self.progress_signal.emit(100)
                self.finished_signal.emit(0)
                return

            for index, em in enumerate(emulator.ldplayer, start=1):
                self.emulator_signal.emit({
                    "index": index,
                    "em": em,
                })

                percent = int((index / total) * 100)
                self.progress_signal.emit(percent)
                self.msleep(50)

            self.finished_signal.emit(total)

        except Exception as e:
            self.error_signal.emit(str(e))