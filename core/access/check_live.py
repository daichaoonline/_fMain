from PyQt6.QtCore import pyqtSignal, QObject
import requests


class CheckLive(QObject):
    check_live = pyqtSignal(str, str)

    def __init__(self, uid):
        super().__init__()
        self.uid = uid

    def run(self):
        checking = self.check_live_uid()
        self.check_live.emit(self.uid, checking)
        return checking

    def check_live_uid(self):
        try:
            url = f'https://graph.facebook.com/{self.uid}/picture?type=normal'
            response = requests.get(url)
            current_url = response.request.url
            if len(current_url) < 200:
                return "Checkpoint"
            return "Live"
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return "Timeout"
        except Exception as e:
            return str(e)