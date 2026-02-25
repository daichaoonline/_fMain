from turtle import st

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QPushButton, QMainWindow
from .stylesheet import *

class ThemeSelector:
    def __init__(self, main_window: QMainWindow, func_save: str):
        self.main_window = main_window
        self.active_theme_name = None
        self.func_save = func_save
        
    def build_widget(self):
        self.grbTheme = QGroupBox("Theme Selector")
        self.grbTheme.setStyleSheet("color: #0d6e7a;")
        themeLayout = QHBoxLayout(self.grbTheme)

        themes = [
            ("Light", StylesLight.light),
            ("Dracula", StylesDracula.dracula),
            ("Coral", StylesCoral.coral),
            ("Golden", StylesGolden.golden),
            ("Ocean", StylesOcean.ocean),
            ("Forest", StylesForest.forest),
        ]

        self.theme_buttons = {}
        for label, style_func in themes:
            btn = QPushButton(label)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(style_func())
            btn.clicked.connect(lambda checked, l=label, s=style_func: self.update_theme(l, s))
            themeLayout.addWidget(btn)
            self.theme_buttons[label] = btn

        return self.grbTheme

    def update_theme(self, label, style_func):
        self.active_theme_name = label
        self.main_window.setStyleSheet(style_func())
        self.func_save