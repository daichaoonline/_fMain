from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QApplication, QMessageBox, QLineEdit, QPushButton,
    QLabel, QWidget)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer, Qt
import pyotp

class TwoFactorAuth(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("2FA Code Generator")
        self.setFixedSize(680, 360)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Secret input section
        secret_section = self.create_secret_input_section()
        main_layout.addWidget(secret_section)

        # Divider
        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #ccc;")
        main_layout.addWidget(divider)

        # Code display section
        code_section = self.create_code_display_section()
        main_layout.addWidget(code_section)

        # Timer to update 2FA code
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_code)
        self.timer.start(1000)

        self.current_totp = None
        self.secret_input.textChanged.connect(self.generate_code)

    def create_secret_input_section(self):
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(8)

        label = QLabel("2FA Secret")
        label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(label)

        subtext = QLabel("Get code for 2 factor authentication easiest - Please store your 2FA secret safely")
        subtext.setFont(QFont("Arial", 8))
        subtext.setStyleSheet("color: #666;")
        subtext.setWordWrap(True)
        layout.addWidget(subtext)

        self.secret_input = QLineEdit()
        self.secret_input.setPlaceholderText("BK5V TV07 D2RB...")
        layout.addWidget(self.secret_input)

        submit_btn = QPushButton("Submit")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        submit_btn.clicked.connect(self.generate_code)
        layout.addWidget(submit_btn)

        return section

    def create_code_display_section(self):
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(8)

        label = QLabel("2FA Code")
        label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(label)

        subtext = QLabel("2-step verification code")
        subtext.setFont(QFont("Arial", 8))
        subtext.setStyleSheet("color: #666;")
        layout.addWidget(subtext)

        self.code_display = QLabel("------")
        self.code_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.code_display.setFixedHeight(60)
        self.code_display.setStyleSheet(self.get_code_style(normal=True))
        layout.addWidget(self.code_display)

        copy_btn = QPushButton("Copy")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #19284D;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        copy_btn.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(copy_btn)

        return section

    def get_code_style(self, normal=True):
        color = "#2c3e50" if normal else "#e74c3c"
        return f"""
            font-size: 24px;
            font-weight: bold;
            color: {color};
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
        """

    def generate_code(self):
        key = self.secret_input.text().replace(" ", "")
        if key:
            try:
                self.current_totp = pyotp.TOTP(key)
                self.update_code()
            except Exception:
                self.current_totp = None

    def update_code(self):
        try:
            if self.current_totp:
                code = self.current_totp.now()
                self.code_display.setText(code)
                seconds_remaining = 30 - (int(pyotp.utils.time.time()) % 30)
                is_expiring = seconds_remaining < 10
                self.code_display.setStyleSheet(self.get_code_style(normal=not is_expiring))
        except Exception:
            return False

    def copy_to_clipboard(self):
        code = self.code_display.text()
        if code and code != "------":
            QApplication.clipboard().setText(code)
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Copied")
            msg_box.setText(f"2FA code {code} copied to clipboard!")
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()