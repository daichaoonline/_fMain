from PyQt6.QtCore import pyqtSignal, QObject


class TimerSignals(QObject): # Signals for the timer
    stop = pyqtSignal()
    start = pyqtSignal()


class TableSignals(QObject): # Signals for the table
    update_row = pyqtSignal(int, list)
    remove_row = pyqtSignal(int)


class MessageSignals(QObject): # Signals for the message box
    warning = pyqtSignal(str, str)
    info = pyqtSignal(str, str)
    critical = pyqtSignal(str, str)


Timer = TimerSignals()
Table = TableSignals()
Message = MessageSignals()