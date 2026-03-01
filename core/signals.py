from PyQt6.QtCore import pyqtSignal, QObject


class TimerSignals(QObject): # Signals for the timer
    stop = pyqtSignal()
    start = pyqtSignal()


class MessageSignals(QObject): # Signals for the message box
    warning = pyqtSignal(str, str)
    info = pyqtSignal(str, str)
    critical = pyqtSignal(str, str)


Timer = TimerSignals()
Message = MessageSignals()