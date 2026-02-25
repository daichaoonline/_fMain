from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import Qt, QUrl

class AboutDialog(QDialog):
    def __init__(self, title, expiry_date, version, developer, copyright, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About HFarm Reels")
        self.setFixedSize(350, 280)
        self.title = title
        self.expiry_date = expiry_date
        self.version = version
        self.developer = developer
        self.copyright = copyright
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(25, 20, 25, 20)

        # Info Section
        expiry_str = self.expiry_date.strftime("%Y-%m-%d") if self.expiry_date else "Lifetime"

        info_text = (
            f"<div style='text-align: center;'>"
            f"<h2 style='color: #0d6e7a; margin-bottom: 0;'>{self.title}</h2>"
            f"<p style='color: #666; margin-top: 0;'>Version {self.version}</p>"
            f"<p style='font-size: 11px; color: #888;'>Developed by <b>{self.developer}</b></p>"
            f"<hr style='border: 0; border-top: 1px solid #eee;'>"
            f"<p style='margin-top: 10px;'><b>License Status:</b><br>"
            f"<span style='color: #e67e22; font-size: 14px; font-weight: bold;'>{expiry_str}</span></p>"
            f"</div>"
        )

        self.lblInfo = QLabel(info_text)
        self.lblInfo.setTextFormat(Qt.TextFormat.RichText)
        self.lblInfo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.lblInfo)

        # Action Buttons (Telegram)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btnTelegram = QPushButton("Telegram")
        self.btnTelegram.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btnTelegram.setStyleSheet("""
            QPushButton {
                background-color: #0088cc; 
                color: white; 
                font-weight: bold; 
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton:hover { background-color: #0099de; }
        """)
        self.btnTelegram.clicked.connect(self.open_telegram_channel)

        btn_layout.addWidget(self.btnTelegram)
        main_layout.addLayout(btn_layout)

        # Copyright
        self.lblCopyright = QLabel(self.copyright)
        self.lblCopyright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblCopyright.setStyleSheet("color: #999; font-size: 10px;")
        main_layout.addWidget(self.lblCopyright)

        # Close button
        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.accept)
        main_layout.addWidget(self.btn_close)

    def open_telegram_channel(self):
        QDesktopServices.openUrl(QUrl("https://t.me/dai_chao_online"))