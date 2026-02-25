from PyQt6.QtCore import QThread, pyqtSignal
from thw_emulator import EmulatorManager

class EmulatorPopulator(QThread):
    update_row_signal = pyqtSignal(int, object)
    finished_signal = pyqtSignal(int)
    error_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, ld_directory: str):
        super().__init__()
        self.ld_directory = ld_directory

    def run(self):
        try:
            emulator = EmulatorManager(self.ld_directory)
            total = len(emulator.ldplayer)

            if total == 0:
                self.progress_signal.emit(100)
                self.finished_signal.emit(0)
                return

            for index, em in enumerate(emulator.ldplayer, start=1):
                self.update_row_signal.emit(index - 1, em)
                percent = int((index / total) * 100)
                self.progress_signal.emit(percent)
                self.msleep(50)

            self.finished_signal.emit(total)

        except Exception as e:
            self.error_signal.emit(str(e))