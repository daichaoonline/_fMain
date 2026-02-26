import names
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
    QMessageBox, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QLabel, QTextEdit, QCompleter)
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import QStringListModel, Qt

class CategoriesPages(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Category & Name Generator")
        self.resize(640, 400)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        categories_group = QGroupBox("Categories")
        categories_layout = QVBoxLayout(categories_group)
        categories_layout.setSpacing(10)

        top_row = QHBoxLayout()
        self.textEdit_categories = QTextEdit()
        self.textEdit_categories.setPlaceholderText("Gamer, TV & Movies, Video Creator")
        self.textEdit_categories.setMinimumHeight(60)

        self.pushButton_refresh = QPushButton("Refresh")
        self.pushButton_refresh.setStyleSheet("QPushButton { background-color: #555555; color: white; }")
        self.pushButton_refresh.setFixedWidth(100)
        self.pushButton_refresh.clicked.connect(self.refresh_categories)

        top_row.addWidget(self.textEdit_categories, 1)
        top_row.addWidget(self.pushButton_refresh)
        categories_layout.addLayout(top_row)

        search_row = QHBoxLayout()
        self.lineEdit_searchCategories = QLineEdit()
        self.lineEdit_searchCategories.setPlaceholderText("Search categories...")

        self.pushButton_apply = QPushButton("Apply")
        self.pushButton_apply.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.pushButton_apply.setEnabled(False)
        self.pushButton_apply.setFixedWidth(100)
        self.pushButton_apply.clicked.connect(self.apply_categories)

        search_row.addWidget(self.lineEdit_searchCategories, 1)
        search_row.addWidget(self.pushButton_apply)
        categories_layout.addLayout(search_row)
        main_layout.addWidget(categories_group)

        name_group = QGroupBox("Name Generator")
        name_layout = QHBoxLayout(name_group)
        name_layout.setSpacing(15)

        self.textEdit_names = QTextEdit()
        self.textEdit_names.setPlaceholderText("Generated names will appear here...")
        self.textEdit_names.setMinimumHeight(150)
        name_layout.addWidget(self.textEdit_names, 1)

        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(10)

        controls_layout.addWidget(QLabel("Count:"))
        self.spinBox_limitNameGen = QSpinBox()
        self.spinBox_limitNameGen.setRange(1, 1000)
        self.spinBox_limitNameGen.setValue(10)
        controls_layout.addWidget(self.spinBox_limitNameGen)

        controls_layout.addWidget(QLabel("Name Type:"))
        self.comboBox_nameType = QComboBox()
        self.comboBox_nameType.addItems(["Full Name", "First Name", "Last Name"])
        controls_layout.addWidget(self.comboBox_nameType)

        self.pushButton_generateNames = QPushButton("Generate Names")
        self.pushButton_generateNames.setStyleSheet("QPushButton { background-color: #555555; color: white; }")
        self.pushButton_generateNames.clicked.connect(self.generate_names)
        controls_layout.addWidget(self.pushButton_generateNames)

        self.pushButton_clearNames = QPushButton("Clear Names")
        self.pushButton_clearNames.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
        self.pushButton_clearNames.clicked.connect(lambda: self.textEdit_names.clear())
        controls_layout.addWidget(self.pushButton_clearNames)

        controls_layout.addStretch(1)
        name_layout.addLayout(controls_layout)
        main_layout.addWidget(name_group)

        self.categories = {
            "Sports team",
            "Movie Theater",
            "Home decor",
            "Food & Drink",
            "Graphic Designer",
            "Digital creator",
            "Discount Store",
            "Diner",
            "Gaming video creator",
            "Music video",
            "Photography Videography",
            "Video Game",
            "Video Game Designer",
            "Video Game Programmer",
            "Entertainment website",
            "Engineering Service",
            "Real Estate",
            "Restaurant",
            "Environmental Conservation Organization"
        }

        self.model = QStringListModel(sorted(self.categories))
        self.completer = QCompleter(self.model, self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.lineEdit_searchCategories.setCompleter(self.completer)

        self.lineEdit_searchCategories.textChanged.connect(self.toggle_apply_button)
        self.lineEdit_searchCategories.returnPressed.connect(self.add_search_category)
        self.completer.activated[str].connect(self.add_category)
        self.textEdit_categories.textChanged.connect(self.toggle_apply_button)

    def toggle_apply_button(self):
        self.pushButton_apply.setEnabled(bool(self.textEdit_categories.toPlainText().strip()) or bool(self.lineEdit_searchCategories.text().strip()))

    def refresh_categories(self):
        self.textEdit_categories.clear()

    def apply_categories(self):
        categories, names_list = self.get_categories_and_names()
        if not categories and not names_list:
            return

        reply = QMessageBox.question(self, "Confirm Apply", "Do you want to apply these categories and names?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.accept()
        else:
            self.reject()

    def add_search_category(self):
        text = self.lineEdit_searchCategories.text().strip()
        if text:
            self.add_category(text)
            self.lineEdit_searchCategories.clear()

    def add_category(self, category):
        current = [c.strip() for c in self.textEdit_categories.toPlainText().split(",") if c.strip()]
        if category not in current:
            current.append(category)
        self.textEdit_categories.setPlainText(", ".join(current))
        self.lineEdit_searchCategories.clear()

    def generate_names(self):
        count = self.spinBox_limitNameGen.value()
        name_type = self.comboBox_nameType.currentText()

        if name_type == "Full Name":
            generated = [f"{names.get_first_name()} {names.get_last_name()}" for _ in range(count)]
        elif name_type == "First Name":
            generated = [names.get_first_name() for _ in range(count)]
        else:
            generated = [names.get_last_name() for _ in range(count)]

        self.textEdit_names.setPlainText("\n".join(generated))
        self.textEdit_names.moveCursor(QTextCursor.MoveOperation.Start)

    def get_categories_and_names(self):
        categories = [c.strip() for c in self.textEdit_categories.toPlainText().split(",") if c.strip()]
        names_list = [n.strip() for n in self.textEdit_names.toPlainText().split("\n") if n.strip()]
        return categories, names_list