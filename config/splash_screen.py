from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QThread, QPropertyAnimation
from PyQt6.QtGui import QPixmap
from core.google import ResourceItems
from modules.selected_items import ItemsGoogle
import os

class SplashScreen(QWidget):
    finished = pyqtSignal()

    def __init__(self, missing_items):
        super().__init__()
        self.setFixedSize(400, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        self.lblIcon = QLabel()
        self.lblIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pix = QPixmap("./recycle.ico")
        if pix.isNull():
            pix = QPixmap(48, 48)
            pix.fill(Qt.GlobalColor.gray)
        self.lblIcon.setPixmap(pix.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(self.lblIcon)

        self.label = QLabel("Starting...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(12)
        layout.addWidget(self.progress_bar)

        self.pulse_animation = QPropertyAnimation(self.lblIcon, b"geometry")
        self.pulse_animation.setDuration(1000)
        self.pulse_animation.setStartValue(QRect(176, 30, 48, 48))
        self.pulse_animation.setKeyValueAt(0.5, QRect(176, 25, 48, 48))
        self.pulse_animation.setEndValue(QRect(176, 30, 48, 48))
        self.pulse_animation.setLoopCount(-1)
        self.pulse_animation.start()

        self.threads = QThread()
        self.worker = ResourceItems(missing_items)
        self.worker.moveToThread(self.threads)

        self.threads.started.connect(self.worker.run)
        self.worker.progress_changed.connect(self.progress_bar.setValue)
        self.worker.status_changed.connect(self.label.setText)
        self.worker.finished.connect(self.on_finished)
        self.worker.finished.connect(self.threads.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.threads.finished.connect(self.threads.deleteLater)
        self.threads.start()

    def on_finished(self):
        self.label.setText("Application Ready!")
        self.pulse_animation.stop()
        self.finished.emit()
        self.close()


class AppSplashScreen:
    def __init__(self):
        self.missing_items = [
            item for item in ItemsGoogle.item_path if not os.path.exists(item["path"])
        ]
        self.splash = None
        self.main = None

    def start(self):
        if self.missing_items:
            self.splash = SplashScreen(self.missing_items)
            self.splash.finished.connect(self.launch_main)
            self.splash.show()
        else:
            self.launch_main()

    def launch_main(self):
        from main import MainWindow
        self.main = MainWindow()
        self.main.show()