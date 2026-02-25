import sys
import subprocess
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox,
    QCheckBox, QTextEdit, QGroupBox
)
from PyQt6.QtCore import Qt

SETTINGS_FILE = "assets/convert.json"

class UiConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 UI Converter")
        self.setFixedSize(700, 450)

        # Title
        self.labelTitle = QLabel("PyQt6 UI Converter")
        self.labelTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Source folder
        self.lineEdit_sourcePath = QLineEdit()
        self.lineEdit_sourcePath.setPlaceholderText("Select folder containing .ui files...")
        self.btnBrowseUI = QPushButton("Browse Folder")
        folderLayout = QHBoxLayout()
        folderLayout.addWidget(self.lineEdit_sourcePath)
        folderLayout.addWidget(self.btnBrowseUI)

        # UI files combo box
        self.comboBox_uiFiles = QComboBox()
        comboLayout = QHBoxLayout()
        comboLayout.addWidget(QLabel("UI Files:"))
        comboLayout.addWidget(self.comboBox_uiFiles)

        # Output path
        self.lineEdit_outputPath = QLineEdit()
        self.lineEdit_outputPath.setPlaceholderText("Output path will appear here...")
        outputLayout = QHBoxLayout()
        outputLayout.addWidget(QLabel("Output:"))
        outputLayout.addWidget(self.lineEdit_outputPath)

        # Options
        optionsGroup = QGroupBox("Options")
        self.checkConvertAll = QCheckBox("Convert All .ui Files in Folder")
        optionsLayout = QVBoxLayout()
        optionsLayout.addWidget(self.checkConvertAll)
        optionsGroup.setLayout(optionsLayout)

        # Convert button
        self.btnConvert = QPushButton("Convert Now")
        self.btnConvert.setStyleSheet("font-weight: bold; height: 30px;")
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.btnConvert)

        # Status and log
        self.statusLabel = QLabel("Status: Ready")
        self.logBox = QTextEdit()
        self.logBox.setReadOnly(True)

        # Main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.labelTitle)
        mainLayout.addLayout(folderLayout)
        mainLayout.addLayout(comboLayout)
        mainLayout.addLayout(outputLayout)
        mainLayout.addWidget(optionsGroup)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(self.logBox)

        # Signals
        self.btnBrowseUI.clicked.connect(self.browse_ui_folder)
        self.lineEdit_sourcePath.textChanged.connect(self.auto_populate_on_input)
        self.comboBox_uiFiles.currentTextChanged.connect(self.update_ui_selection)
        self.btnConvert.clicked.connect(self.convert_ui)

        # Load last settings
        self.load_settings()

    # Browse folder
    def browse_ui_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select UI Folder", self.lineEdit_sourcePath.text())
        if folder:
            self.lineEdit_sourcePath.setText(folder)

    # Auto populate combo box
    def auto_populate_on_input(self, folder):
        if os.path.isdir(folder):
            self.populate_ui_files(folder)

    # Populate combo box with .ui files
    def populate_ui_files(self, folder):
        self.comboBox_uiFiles.blockSignals(True)
        self.comboBox_uiFiles.clear()
        try:
            ui_files = [f for f in os.listdir(folder) if f.endswith(".ui")]
            if ui_files:
                self.comboBox_uiFiles.addItems(ui_files)
                self.comboBox_uiFiles.blockSignals(False)
                self.update_ui_selection(self.comboBox_uiFiles.currentText())
            else:
                self.comboBox_uiFiles.blockSignals(False)
                self.statusLabel.setText("Status: No .ui files found in directory.")
        except Exception as e:
            self.logBox.append(f"[ERROR] Could not read folder: {str(e)}")

    # Update output path based on selected UI file
    def update_ui_selection(self, filename):
        folder = self.lineEdit_sourcePath.text()
        if folder and filename:
            output_folder = os.path.join(folder, "ui", "generated")
            os.makedirs(output_folder, exist_ok=True)
            py_file_name = os.path.splitext(filename)[0] + ".py"
            py_path = os.path.join(output_folder, py_file_name)
            py_path = py_path.replace("\\", "/")  # Forward slashes
            self.lineEdit_outputPath.setText(py_path)

    # Convert UI files
    def convert_ui(self):
        folder = self.lineEdit_sourcePath.text().strip()
        if not os.path.isdir(folder):
            QMessageBox.warning(self, "Error", "Valid folder path required.")
            return

        output_root = os.path.join(folder, "ui", "generated")
        os.makedirs(output_root, exist_ok=True)

        if self.checkConvertAll.isChecked():
            ui_files = [f for f in os.listdir(folder) if f.endswith(".ui")]
            if not ui_files:
                self.statusLabel.setText("Status: No .ui files to convert.")
                return
            for ui_file in ui_files:
                py_path = os.path.join(output_root, os.path.splitext(ui_file)[0] + ".py").replace("\\", "/")
                self.convert_single(os.path.join(folder, ui_file), py_path)
            self.statusLabel.setText(f"Status: Bulk conversion complete ({len(ui_files)} files).")
        else:
            selected_file = self.comboBox_uiFiles.currentText()
            if not selected_file:
                QMessageBox.warning(self, "Error", "Select a UI file to convert.")
                return
            ui_path = os.path.join(folder, selected_file)
            py_path = self.lineEdit_outputPath.text()
            self.convert_single(ui_path, py_path)
            self.statusLabel.setText("Status: Single conversion complete.")

        self.save_settings()

    # Convert a single .ui file
    def convert_single(self, ui_path, py_path):
        try:
            subprocess.run(
                ["pyuic6", "-x", ui_path, "-o", py_path],
                check=True
            )
            self.logBox.append(f"[OK] {os.path.basename(ui_path)} → {py_path}")
            self.logBox.verticalScrollBar().setValue(self.logBox.verticalScrollBar().maximum())
        except Exception as e:
            self.logBox.append(f"[FAIL] {os.path.basename(ui_path)}: {str(e)}")
            self.logBox.verticalScrollBar().setValue(self.logBox.verticalScrollBar().maximum())

    # Load settings from JSON
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    settings = json.load(f)
                last_folder = settings.get("last_folder", "")
                if os.path.isdir(last_folder):
                    self.lineEdit_sourcePath.setText(last_folder)
                self.checkConvertAll.setChecked(settings.get("convert_all", False))
            except Exception as e:
                self.logBox.append(f"[WARN] Could not load settings: {str(e)}")

    # Save settings to JSON
    def save_settings(self):
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        settings = {
            "last_folder": self.lineEdit_sourcePath.text(),
            "convert_all": self.checkConvertAll.isChecked()
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UiConverter()
    win.show()
    sys.exit(app.exec())