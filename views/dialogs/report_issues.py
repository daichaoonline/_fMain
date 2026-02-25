from dataclasses import dataclass
import requests
from PyQt6.QtWidgets import (
    QApplication, QDialog, QTextEdit, QPushButton, QVBoxLayout, 
    QMessageBox, QLabel, QHBoxLayout
)
import sys

@dataclass
class ReportIssues:
    bot_token: str
    chat_id: str
    parent: object = None

    def report(self):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        message = self.get_user_message()
        if not message:
            return

        try:
            text_message = f"<code>{message}</code>"
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": text_message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=data)

            if response.status_code == 200:
                self.show_message("Success", "Message sent successfully.", QMessageBox.Icon.Information)
            else:
                self.show_message("Failed", f"Failed to send message:\n{response.text}", QMessageBox.Icon.Warning)

        except Exception as e:
            self.show_message("Error", f"An error occurred:\n{e}", QMessageBox.Icon.Critical)

    def get_user_message(self):
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Report Issue")
        dialog.setModal(True)
        dialog.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Type your issue message below:"))

        text_edit = QTextEdit()
        text_edit.setPlaceholderText("Describe the issue here...")
        layout.addWidget(text_edit)

        btn_ok = QPushButton("Send")
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(dialog.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            raw_text = text_edit.toPlainText().strip()
            if not raw_text:
                return None

            normalized_text = "\n".join(line.strip() for line in raw_text.splitlines() if line.strip())
            return normalized_text

        return None

    def show_message(self, title, text, icon):
        msg = QMessageBox(self.parent)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.exec()