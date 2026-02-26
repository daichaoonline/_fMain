from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel)

class Category(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Category")
        self.setMinimumWidth(300)
        self.main_layout = QVBoxLayout(self)

        self.label_categoryName = QLabel("Category Name:")
        self.lineEdit_categoryName = QLineEdit()
        self.lineEdit_categoryName.setPlaceholderText("Enter category name")

        self.button_layout = QHBoxLayout()
        self.pushButton_okay = QPushButton("OK")
        self.pushButton_cancel = QPushButton("Cancel")

        self.button_layout.addWidget(self.pushButton_okay)
        self.button_layout.addWidget(self.pushButton_cancel)

        self.main_layout.addWidget(self.label_categoryName)
        self.main_layout.addWidget(self.lineEdit_categoryName)
        self.main_layout.addLayout(self.button_layout)

        self.pushButton_okay.clicked.connect(self.accept)
        self.pushButton_cancel.clicked.connect(self.reject)

    def get_category_name(self):
        return self.lineEdit_categoryName.text().strip()