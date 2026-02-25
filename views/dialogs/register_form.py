import os
from PyQt6.QtWidgets import QDialog, QMessageBox
from license_system import HardwareManager, LicenseKeys, TelegramNotifier
from views.forms import fmRegister
    
class RegisterForm(QDialog, fmRegister):
    def __init__(self, license_manager: LicenseKeys, telegram: TelegramNotifier, parent=None):
        super().__init__(parent)    
        self.setupUi(self)
        self.license_manager = license_manager
        self.telegram_bot = telegram
        self.setup_hardware_info()
        
        self.btnRegister.clicked.connect(self.register_user)
        self.btnCancel.clicked.connect(self.reject)

    def setup_hardware_info(self):
        hwd_manager = HardwareManager()
        hwd_id = hwd_manager.get_hardware()
        site_code = hwd_id[:8].upper()
        self.valMachineID.setText(hwd_id)
        self.valSiteCode.setText(site_code)

    def register_user(self):
        email = self.editEmail.text().strip()
        if not email or "@" not in email:
            QMessageBox.warning(self, "Error", "A valid Email is required!")
            return

        self.license_manager.check_or_generate_license()
        license_file = "license.txt"
        license_info = ""

        if os.path.exists(license_file):
            with open(license_file, encoding="utf-8") as f:
                license_info = f.read().strip()

        if "|" in license_info:
            parts = license_info.split("|")
            key_value = parts[0].replace("Key:", "").strip()
            hwd_value = parts[1].replace("HWD:", "").strip()
            self.editSerial.setText(key_value)

        message = (
            f"🆕 **New Registration**\n"
            f"📧 Email: {email}\n"
            f"🔑 License: {license_info}\n"
            f"💻 ID: {self.valMachineID.text()}"
        )
        
        self.telegram_bot.send_message(message)
        QMessageBox.information(self, "Success", "Registration sent successfully!")
        self.accept()