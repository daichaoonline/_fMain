from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QComboBox, QPushButton,
    QMessageBox, QTextEdit, QCheckBox, QButtonGroup)
import json
import os

class AllowBlock(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("IP Manager")
        self.setMinimumSize(450, 350)
        self.countries = ["UK", "Germany", "France", "China", "India", "KH", "Thailand"]

        self.appdata = os.getenv("APPDATA")
        self.config = os.path.join(self.appdata, ".temp", "allow_block.json")
        os.makedirs(os.path.dirname(self.config), exist_ok=True)
        self.last_config = None
        self.init_ui()
        self.read_config()

    def init_ui(self):
        layout = QVBoxLayout()
        hbox_check = QHBoxLayout()
        self.checkBox_allow = QCheckBox("Allow IP/Country")
        self.checkBox_block = QCheckBox("Block IP/Country")
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.button_group.addButton(self.checkBox_allow)
        self.button_group.addButton(self.checkBox_block)
        hbox_check.addWidget(self.checkBox_allow)
        hbox_check.addWidget(self.checkBox_block)
        layout.addLayout(hbox_check)

        layout.addWidget(QLabel("Enter IPs or Countries (one per line):"))
        self.textEdit_list = QTextEdit()
        layout.addWidget(self.textEdit_list)

        layout.addWidget(QLabel("Select Country:"))
        combo_layout = QHBoxLayout()
        self.comboBox_list = QComboBox()
        self.comboBox_list.addItems(self.countries)
        self.comboBox_list.currentTextChanged.connect(self.append_country_to_text)
        combo_layout.addWidget(self.comboBox_list)

        self.lineEdit_newCountry = QLineEdit()
        self.lineEdit_newCountry.setPlaceholderText("Add new country")
        self.pushButton_addCountry = QPushButton("Add")
        self.pushButton_addCountry.clicked.connect(self.add_country)
        combo_layout.addWidget(self.lineEdit_newCountry)
        combo_layout.addWidget(self.pushButton_addCountry)
        layout.addLayout(combo_layout)

        button_layout = QHBoxLayout()
        self.pushButton_apply = QPushButton("Apply")
        self.pushButton_apply.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.pushButton_cancel = QPushButton("Cancel")
        self.pushButton_cancel.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
        self.pushButton_apply.clicked.connect(self.apply_rules)
        self.pushButton_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.pushButton_apply)
        button_layout.addWidget(self.pushButton_cancel)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_country(self):
        new_country = self.lineEdit_newCountry.text().strip()
        if new_country and new_country not in self.countries:
            self.countries.append(new_country)
            self.comboBox_list.addItem(new_country)
            self.lineEdit_newCountry.clear()
        else:
            QMessageBox.warning(self, "Warning", "Country is empty or already exists.")

    def append_country_to_text(self, country):
        if country.strip() and country not in self.textEdit_list.toPlainText().splitlines():
            current_text = self.textEdit_list.toPlainText()
            if current_text:
                self.textEdit_list.append(country)
            else:
                self.textEdit_list.setPlainText(country)

    def apply_rules(self):
        allow_checked = self.checkBox_allow.isChecked()
        block_checked = self.checkBox_block.isChecked()
        ip_list = [line.strip() for line in self.textEdit_list.toPlainText().splitlines() if line.strip()]
        selected_country = self.comboBox_list.currentText()

        config = {"allow": allow_checked, "block": block_checked, "ip_list": ip_list, "countries": self.countries, "selected_country": selected_country}
        self.write_config(config)
        self.last_config = config
        self.accept()

    def read_config(self):
        if os.path.exists(self.config):
            with open(self.config, "r") as f:
                config = json.load(f)
            self.checkBox_allow.setChecked(config.get("allow", False))
            self.checkBox_block.setChecked(config.get("block", False))
            self.textEdit_list.setPlainText("\n".join(config.get("ip_list", [])))
            self.countries = config.get("countries", self.countries)
            self.comboBox_list.clear()
            self.comboBox_list.addItems(self.countries)
            selected = config.get("selected_country")
            if selected and selected in self.countries:
                self.comboBox_list.setCurrentText(selected)

    def write_config(self, config):
        with open(self.config, "w") as f:
            json.dump(config, f, indent=4)

    def get_config(self):
        if self.last_config:
            return self.last_config
        return {"allow": self.checkBox_allow.isChecked(), "block": self.checkBox_block.isChecked(), "ip_list": [line.strip() for line in self.textEdit_list.toPlainText().splitlines() if line.strip()], "countries": self.countries, "selected_country": self.comboBox_list.currentText()}

    def get_allowed_ips(self):
        if not self.checkBox_allow.isChecked():
            return []
        return [line.strip() for line in self.textEdit_list.toPlainText().splitlines() if line.strip()]

    def get_blocked_ips(self):
        if not self.checkBox_block.isChecked():
            return []
        return [line.strip() for line in self.textEdit_list.toPlainText().splitlines() if line.strip()]