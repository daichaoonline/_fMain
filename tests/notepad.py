from PyQt6.QtWidgets import QTableWidget
from dataclasses import dataclass

@dataclass
class TableWidget:
    tableWidget: QTableWidget
    
    def __post__init__(self):
        widths = [100, 200, 150]
        for i, w in enumerate(widths):
            self.tableWidget.setColumnWidth(i, w)
            
            

    # QMainWindow { background-color: #f8f9f8; }
    # QFrame#topNav { background-color: #ffffff; border-bottom: 1px solid #e0e0e0; }
    # QLabel#logoText { color: #76ba1b; font-weight: bold; font-size: 20px; }
    # QPushButton { border-radius: 4px; border: 1px solid #dcdcdc; padding: 5px; }
    # QPushButton#btnStart { background-color: #76ba1b; color: white; font-weight: bold; border: none; }
    # QPushButton#btnStop { background-color: #e35d6a; color: white; font-weight: bold; border: none; }
    # QHeaderView::section { background-color: #76ba1b; color: white; padding: 5px; font-weight: bold; border: 1px solid #68a318; }
    # QTableWidget { background-color: white; alternate-background-color: #f2f9eb; gridline-color: #e0e0e0; }
    # QLineEdit, QComboBox { border: 1px solid #76ba1b; border-radius: 3px; }
   