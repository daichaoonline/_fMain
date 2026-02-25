import requests
import webbrowser
from dataclasses import dataclass
from typing import Optional
from packaging import version
from PyQt6.QtWidgets import QMessageBox

@dataclass(frozen=True)
class UpdateInfo:
    latest_version: str
    changelog: str
    download_url: str

class CheckUpdates:
    def __init__(self, current_version: str, json_url: str, parent=None):
        self.current_version = current_version
        self.json_url = json_url
        self.parent = parent

    def fetch_update_data(self) -> Optional[UpdateInfo]:
        try:
            response = requests.get(self.json_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return UpdateInfo(
                latest_version=data['version'],
                changelog=data['changelog'],
                download_url=data['url']
            )
        except (requests.RequestException, ValueError) as e:
            return None

    def check_for_updates(self, silent_if_latest: bool = False):
        update_data = self.fetch_update_data()
        if not update_data:
            self._show_error_dialog("Connection Error", "Could not reach the update server.")
            return

        is_newer = version.parse(update_data.latest_version) > version.parse(self.current_version)

        if is_newer:
            self._show_update_dialog(update_data)
        elif not silent_if_latest:
            self._show_info_dialog("Up to Date", f"You are using the latest version (v{self.current_version}).")

    def _show_update_dialog(self, info: UpdateInfo):
        msg = QMessageBox(self.parent)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Update Available")
        msg.setText(f"<h3>A new version ({info.latest_version}) is available!</h3>")
        msg.setInformativeText(f"<b>What's New:</b>\n{info.changelog}")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)

        if msg.exec() == QMessageBox.StandardButton.Ok:
            if info.download_url:
                webbrowser.open(info.download_url)

    def _show_error_dialog(self, title: str, message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def _show_info_dialog(self, title: str, message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()