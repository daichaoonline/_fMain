import re
import os
import requests
from PyQt6.QtCore import QObject, pyqtSignal, QThread

class GoogleDrive:
    @staticmethod
    def download_file(gdrive_id, destination_path, progress_callback=None):
        def get_confirm_token(response_text):
            match = re.search(r"confirm=([0-9A-Za-z_]+)", response_text)
            return match.group(1) if match else None

        def download_with_token(session, confirm_token, gdrive_id):
            params = {"export": "download", "id": gdrive_id, "confirm": confirm_token}
            return session.get("https://drive.google.com/uc", params=params, stream=True)

        URL = "https://drive.google.com/uc?export=download"
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        session = requests.Session()
        response = session.get(URL, params={"id": gdrive_id}, stream=True)
        token = get_confirm_token(response.text)
        if token:
            response = download_with_token(session, token, gdrive_id)

        try:
            response.raise_for_status()
            total_length = response.headers.get('content-length')

            if total_length is None:
                with open(destination_path, "wb") as f:
                    f.write(response.content)
                if progress_callback:
                    progress_callback(100)
                return True

            dl = 0
            total_length = int(total_length)
            with open(destination_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)
                        dl += len(chunk)
                        if progress_callback:
                            percent = int(dl / total_length * 100)
                            progress_callback(percent)
            return True
        except Exception as e:
            return f"Error: {e}"

class ResourceItems(QObject):
    progress_changed = pyqtSignal(int)
    status_changed = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, items):
        super().__init__()
        self.required_items = items

    def run(self):
        total_files = len(self.required_items)
        for idx, item in enumerate(self.required_items, start=1):
            path = item["path"]
            gdrive_id = item["gdrive_id"]

            if os.path.exists(path):
                self.status_changed.emit(f"Exists: {os.path.basename(path)}")
                percent = int(idx / total_files * 100)
                self.progress_changed.emit(percent)
                QThread.msleep(50)
                continue

            self.status_changed.emit(f"Downloading: {os.path.basename(path)}")

            def file_progress(p):
                base = (idx - 1) / total_files * 100
                step = 1 / total_files * 100
                overall = int(base + p * step / 100)
                self.progress_changed.emit(overall)

            success = GoogleDrive.download_file(gdrive_id, path, file_progress)
            if not success:
                self.status_changed.emit(f"Failed to download {os.path.basename(path)}")
            QThread.msleep(50)

        self.status_changed.emit("All resources ready!")
        self.progress_changed.emit(100)
        self.finished.emit()