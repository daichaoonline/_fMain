class StylesLight:
    LIGHT = """
        QGroupBox { 
            border:1px solid #cccccc; 
            border-radius:3px; 
            margin-top:15px; 
            padding:2px 2px 2px 2px;
        }
        QGroupBox::title { 
            subcontrol-origin: margin; 
            left:5px; 
            padding: 0 2px; 
            color:#4a90e2; 
            background:transparent;
        }
        
        QLabel#sectionLabel { color:#357ABD; font-weight:600; }
        QLabel#counterLabel { color:#555555; }
        QLabel#idLabel { color:#2d5d9f; font-weight:600; }
        
        QTableWidget, QTreeWidget, QTableView, QListView { 
            background:#ffffff; 
            alternate-background-color:#f2f2f2; 
            gridline-color:#cccccc; 
            border:1px solid #cccccc; 
            selection-background-color:#4a90e2; 
            selection-color:#ffffff;
        }
        QHeaderView::section { 
            background:#e6e6e6; color:#222222; 
            border:0; padding:1px;
        }
        
        QLineEdit, QTextEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QRadioButton { 
            background:#ffffff; border:1px solid #cccccc; border-radius:3px; padding:1px; 
            selection-background-color:#4a90e2;
        }
        
        QCheckBox { spacing:5px; }
        QPushButton { 
            background:#4a90e2; color:white; border:1px solid #357ABD; border-radius:3px; padding: 5px 9px;
        }
        
        QPushButton:hover { background:#357ABD; }
        QPushButton#browseBtn { background:#2d5d9f; }
        QToolButton { 
            background:#4a90e2; color:white; border:1px solid #357ABD; border-radius:3px; 
        }

        QScrollBar {
            border: none;
            background: transparent;
            margin: 0;
        }

        QScrollBar:vertical { width: 7px; }
        QScrollBar:horizontal { height: 7px; }

        QScrollBar::handle {
            background: #cccccc;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical { min-height: 7px; }
        QScrollBar::handle:horizontal { min-width: 7px; }

        QScrollBar::handle:hover {
            background: #999999;
        }

        QScrollBar::add-line,
        QScrollBar::sub-line {
            width: 0;
            height: 0;
        }
             
    """
    
    @classmethod
    def light(cls):
        return cls.LIGHT

class StylesDracula:
    DRACULA = """
        QWidget#page_upload_tools, QWidget { background:#0F2237; color:#e7eef7; }
        
        QGroupBox { 
            border:1px solid #1d3557; 
            border-radius:3px; 
            margin-top:15px; 
            padding:2px 2px 2px 2px;
        }
        QGroupBox::title { 
            subcontrol-origin: margin; 
            left:5px; 
            padding: 0 2px; 
            color:#a8c3ff; 
            background:transparent;
        }
        
        QLabel#sectionLabel { color:#9fc1ff; font-weight:600; }
        QLabel#counterLabel { color:#c8dcff; }
        QLabel#idLabel { color:#6fb1ff; font-weight:600; }
        
        QTableWidget, QTreeWidget, QTableView, QListView { 
            background:#0c1b2c; 
            alternate-background-color:#0e2135; 
            gridline-color:#27486e; 
            border:1px solid #223b5a; 
            selection-background-color:#1b3e6b; 
            selection-color:#ffffff;
        }
        QHeaderView::section { 
            background:#132a45; color:#cbd9ee; 
            border:0; padding:1px;
        }
        
        QLineEdit, QTextEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QRadioButton { 
            background:#0c1b2c; border:1px solid #27486e; border-radius:3px; padding:1px; 
            selection-background-color:#1b3e6b;
        }
        
        QCheckBox { spacing:5px; }
        QPushButton { 
            background:#1e3a5f; border:1px solid #2f4f7a; border-radius:3px; padding: 5px 9px;
        }
        
        QPushButton:hover { background:#254872; }
        QPushButton#browseBtn { background:#153458; }
        QToolButton { 
            background:#173356; border:1px solid #2a4a75; border-radius:3px; 
        }

        QScrollBar {
            border: none;
            background: transparent;
            margin: 0;
        }

        QScrollBar:vertical { width: 7px; }
        QScrollBar:horizontal { height: 7px; }

        QScrollBar::handle {
            background: #303C4A;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical { min-height: 7px; }
        QScrollBar::handle:horizontal { min-width: 7px; }

        QScrollBar::handle:hover {
            background: #a0a0a0;
        }

        QScrollBar::add-line,
        QScrollBar::sub-line {
            width: 0;
            height: 0;
        }
          
        QMenuBar, QMenu { background:#0c1b2c; color:#e7eef7; }
        QMenuBar::item:selected, QMenu::item:selected { background:#132a45; color:#e7eef7; }
    """
    
    @classmethod
    def dracula(cls):
        return cls.DRACULA

class StylesCoral:
    CORAL = """
        QWidget#page_upload_tools, QWidget { background:#fff0f0; color:#c62828; }
        
        QGroupBox { 
            border:1px solid #e57373; 
            border-radius:3px; 
            margin-top:15px; 
            padding:2px 2px 2px 2px;
        }
        QGroupBox::title { 
            subcontrol-origin: margin; 
            left:5px; 
            padding: 0 2px; 
            color:#ef5350; 
            background:transparent;
        }
        
        QLabel#sectionLabel { color:#e53935; font-weight:600; }
        QLabel#counterLabel { color:#c62828; }
        QLabel#idLabel { color:#d32f2f; font-weight:600; }
        
        QTableWidget, QTreeWidget, QTableView, QListView { 
            background:#ffe6e6; 
            alternate-background-color:#fff0f0; 
            gridline-color:#f06292; 
            border:1px solid #e57373; 
            selection-background-color:#ef5350; 
            selection-color:#ffffff;
        }
        QHeaderView::section { 
            background:#f8bbd0; color:#c62828; 
            border:0; padding:1px;
        }
        
        QLineEdit, QTextEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QRadioButton { 
            background:#fff0f0; border:1px solid #e57373; border-radius:3px; padding:1px; 
            selection-background-color:#ef5350;
        }
        
        QCheckBox { spacing:5px; }
        QPushButton { 
            background:#ef5350; color:white; border:1px solid #e57373; border-radius:3px; padding: 5px 9px;
        }
        
        QPushButton:hover { background:#e57373; }
        QPushButton#browseBtn { background:#c62828; color:white; }
        QToolButton { 
            background:#ef5350; color:white; border:1px solid #e57373; border-radius:3px; 
        }

        QScrollBar {
            border: none;
            background: transparent;
            margin: 0;
        }

        QScrollBar:vertical { width: 7px; }
        QScrollBar:horizontal { height: 7px; }

        QScrollBar::handle {
            background: #f06292;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical { min-height: 7px; }
        QScrollBar::handle:horizontal { min-width: 7px; }

        QScrollBar::handle:hover {
            background: #ef5350;
        }

        QScrollBar::add-line,
        QScrollBar::sub-line {
            width: 0;
            height: 0;
        }
        QMenuBar, QMenu { background:#ffe6e6; color:#c62828; }
        QMenuBar::item:selected, QMenu::item:selected { background:#f8bbd0; color:#c62828; }
            
    """
    @classmethod
    def coral(cls):
        return cls.CORAL

class StylesGolden:
    GOLDEN = """
        QWidget#page_upload_tools, QWidget { background:#fff8e7; color:#5a3e00; }
        
        QGroupBox { 
            border:1px solid #d4af37; 
            border-radius:3px; 
            margin-top:15px; 
            padding:2px 2px 2px 2px;
        }
        QGroupBox::title { 
            subcontrol-origin: margin; 
            left:5px; 
            padding: 0 2px; 
            color:#b8860b; 
            background:transparent;
        }
        
        QLabel#sectionLabel { color:#b8860b; font-weight:600; }
        QLabel#counterLabel { color:#7b5a00; }
        QLabel#idLabel { color:#996515; font-weight:600; }
        
        QTableWidget, QTreeWidget, QTableView, QListView { 
            background:#fffdf7; 
            alternate-background-color:#fff7e1; 
            gridline-color:#e6c96b; 
            border:1px solid #e6c96b; 
            selection-background-color:#d4af37; 
            selection-color:#ffffff;
        }
        QHeaderView::section { 
            background:#f6e6b4; color:#5a3e00; 
            border:0; padding:1px;
        }
        
        QLineEdit, QTextEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QRadioButton { 
            background:#ffffff; border:1px solid #e6c96b; border-radius:3px; padding:1px; 
            selection-background-color:#d4af37;
        }
        
        QCheckBox { spacing:5px; }
        QPushButton { 
            background:#d4af37; color:white; border:1px solid #b8860b; border-radius:3px; padding: 5px 9px;
        }
        
        QPushButton:hover { background:#b8860b; }
        QPushButton#browseBtn { background:#996515; color:white; }
        QToolButton { 
            background:#d4af37; color:white; border:1px solid #b8860b; border-radius:3px; 
        }

        QScrollBar {
            border: none;
            background: transparent;
            margin: 0;
        }

        QScrollBar:vertical { width: 7px; }
        QScrollBar:horizontal { height: 7px; }

        QScrollBar::handle {
            background: #e6c96b;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical { min-height: 7px; }
        QScrollBar::handle:horizontal { min-width: 7px; }

        QScrollBar::handle:hover {
            background: #d4af37;
        }

        QScrollBar::add-line,
        QScrollBar::sub-line {
            width: 0;
            height: 0;
        }

        QMenuBar, QMenu { background:#fff8e7; color:#5a3e00; }
        QMenuBar::item:selected, QMenu::item:selected { background:#fff1c2; color:#5a3e00; }  
             
    """
    
    @classmethod
    def golden(cls):
        return cls.GOLDEN

class StylesOcean:
    OCEAN = """
        QWidget#page_upload_tools, QWidget { background:#e0f7fa; color:#006064; }
        
        QGroupBox { 
            border:1px solid #00838f; 
            border-radius:3px; 
            margin-top:15px; 
            padding:2px 2px 2px 2px;
        }
        QGroupBox::title { 
            subcontrol-origin: margin; 
            left:5px; 
            padding: 0 2px; 
            color:#00acc1; 
            background:transparent;
        }
        
        QLabel#sectionLabel { color:#00838f; font-weight:600; }
        QLabel#counterLabel { color:#006064; }
        QLabel#idLabel { color:#004d40; font-weight:600; }
        
        QTableWidget, QTreeWidget, QTableView, QListView { 
            background:#b2ebf2; 
            alternate-background-color:#e0f7fa; 
            gridline-color:#4dd0e1; 
            border:1px solid #00acc1; 
            selection-background-color:#00bcd4; 
            selection-color:#ffffff;
        }
        QHeaderView::section { 
            background:#80deea; color:#004d40; 
            border:0; padding:1px;
        }
        
        QLineEdit, QTextEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QRadioButton { 
            background:#e0f7fa; border:1px solid #00acc1; border-radius:3px; padding:1px; 
            selection-background-color:#00bcd4;
        }
        
        QCheckBox { spacing:5px; }
        QPushButton { 
            background:#00acc1; color:white; border:1px solid #00838f; border-radius:3px; padding: 5px 9px;
        }
        
        QPushButton:hover { background:#00838f; }
        QPushButton#browseBtn { background:#006064; color:white; }
        QToolButton { 
            background:#00acc1; color:white; border:1px solid #00838f; border-radius:3px; 
        }

        QScrollBar {
            border: none;
            background: transparent;
            margin: 0;
        }

        QScrollBar:vertical { width: 7px; }
        QScrollBar:horizontal { height: 7px; }

        QScrollBar::handle {
            background: #26c6da;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical { min-height: 7px; }
        QScrollBar::handle:horizontal { min-width: 7px; }

        QScrollBar::handle:hover {
            background: #00bcd4;
        }

        QScrollBar::add-line,
        QScrollBar::sub-line {
            width: 0;
            height: 0;
        }
        QMenuBar, QMenu { background:#b2ebf2; color:#006064; }
        QMenuBar::item:selected, QMenu::item:selected { background:#80deea; color:#004d40; }
             
    """
    
    @classmethod
    def ocean(cls):
        return cls.OCEAN

class StylesForest:
    FOREST = """
        QWidget#page_upload_tools, QWidget { background:#e8f5e9; color:#1b5e20; }
        
        QGroupBox { 
            border:1px solid #2e7d32; 
            border-radius:3px; 
            margin-top:15px; 
            padding:2px 2px 2px 2px;
        }
        QGroupBox::title { 
            subcontrol-origin: margin; 
            left:5px; 
            padding: 0 2px; 
            color:#388e3c; 
            background:transparent;
        }
        
        QLabel#sectionLabel { color:#2e7d32; font-weight:600; }
        QLabel#counterLabel { color:#1b5e20; }
        QLabel#idLabel { color:#33691e; font-weight:600; }
        
        QTableWidget, QTreeWidget, QTableView, QListView { 
            background:#c8e6c9; 
            alternate-background-color:#e8f5e9; 
            gridline-color:#66bb6a; 
            border:1px solid #2e7d32; 
            selection-background-color:#43a047; 
            selection-color:#ffffff;
        }
        QHeaderView::section { 
            background:#a5d6a7; color:#1b5e20; 
            border:0; padding:1px;
        }
        
        QLineEdit, QTextEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QRadioButton { 
            background:#e8f5e9; border:1px solid #2e7d32; border-radius:3px; padding:1px; 
            selection-background-color:#43a047;
        }
        
        QCheckBox { spacing:5px; }
        QPushButton { 
            background:#43a047; color:white; border:1px solid #2e7d32; border-radius:3px; padding: 5px 9px;
        }
        
        QPushButton:hover { background:#2e7d32; }
        QPushButton#browseBtn { background:#1b5e20; color:white; }
        QToolButton { 
            background:#43a047; color:white; border:1px solid #2e7d32; border-radius:3px; 
        }

        QScrollBar {
            border: none;
            background: transparent;
            margin: 0;
        }

        QScrollBar:vertical { width: 7px; }
        QScrollBar:horizontal { height: 7px; }

        QScrollBar::handle {
            background: #66bb6a;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical { min-height: 7px; }
        QScrollBar::handle:horizontal { min-width: 7px; }

        QScrollBar::handle:hover {
            background: #43a047;
        }

        QScrollBar::add-line,
        QScrollBar::sub-line {
            width: 0;
            height: 0;
        }
        
        QMenuBar, QMenu { background:#c8e6c9; color:#1b5e20; }
        QMenuBar::item:selected, QMenu::item:selected { background:#a5d6a7; color:#1b5e20; }        
    """
    
    @classmethod
    def forest(cls):
        return cls.FOREST
    
class LoadStylesheet:
    def __init__(self, theme_name: str):
        themes = {
            "light": StylesLight.light,
            "dracula": StylesDracula.dracula,
            "coral": StylesCoral.coral,
            "golden": StylesGolden.golden,
            "ocean": StylesOcean.ocean,
            "forest": StylesForest.forest
        }
        
        theme_func = themes.get(theme_name.lower(), StylesLight.light)
        self.content = theme_func() 
        
class Theme_:
    STYLE = """
        QMainWindow { background-color: #f5f7f5; }
        
        /* Top Navigation */
        #nav_bar { background-color: white; border-bottom: 1px solid #ddd; min-height: 50px; }
        QPushButton#nav_btn { background: transparent; color: #333; font-weight: bold; border: none; padding: 10px; }
        QPushButton#nav_btn:hover { color: #76ba1b; }

        /* Buttons and Labels */
        QPushButton#start_btn { background-color: #76ba1b; color: white; border-radius: 4px; font-weight: bold; }
        QPushButton#stop_btn { background-color: #e35d6a; color: white; border-radius: 4px; font-weight: bold; }
        QLabel { color: #333; font-size: 11px; }
        
        /* Tables */
        QTableWidget { background-color: white; border: 1px solid #e0e0e0; gridline-color: #f0f0f0; }
        QHeaderView::section { 
            background-color: #76ba1b; color: white; 
            padding: 5px; border: 1px solid #68a318; font-weight: bold; 
        }
        
        /* Inputs */
        QLineEdit { border: 1px solid #76ba1b; border-radius: 3px; padding: 2px; background: white; }
    """
    
class Theme:
    STYLE = """
        /* Main Window and General */
        QMainWindow { 
            background-color: #f5f7f5; 
        }
        
        QLabel { 
            color: #333; 
            font-size: 11px; 
        }

        /* Top Navigation Bar */
        #nav_bar { 
            background-color: white; 
            border-bottom: 1px solid #ddd; 
            min-height: 50px; 
        }
        
        QPushButton#nav_btn { 
            background: transparent; 
            color: #333; 
            font-weight: bold; 
            border: none; 
            padding: 10px; 
        }
        
        QPushButton#nav_btn:hover { 
            color: #76ba1b; 
        }

        /* Menu Bar (File, Edit, etc.) */
        QMenuBar {
            background-color: white;
            border-bottom: 1px solid #ddd;
            color: #333;
        }

        QMenuBar::item {
            background-color: transparent;
            padding: 5px 12px;
            margin: 2px;
        }

        QMenuBar::item:selected {
            background-color: #f0f0f0;
            color: #76ba1b;
            border-radius: 4px;
        }

        QMenuBar::item:pressed {
            background-color: #76ba1b;
            color: white;
        }

        /* Dropdown Menus */
        QMenu {
            background-color: white;
            border: 1px solid #ddd;
            padding: 4px;
        }

        QMenu::item {
            padding: 6px 30px 6px 20px;
            color: #333;
        }

        QMenu::item:selected {
            background-color: #76ba1b;
            color: white;
            border-radius: 3px;
        }

        QMenu::separator {
            height: 1px;
            background: #eee;
            margin: 4px 10px;
        }

        /* Buttons */
        QPushButton#start_btn { 
            background-color: #76ba1b; 
            color: white; 
            border-radius: 4px; 
            font-weight: bold; 
            padding: 5px 15px;
        }
        
        QPushButton#start_btn:hover {
            background-color: #68a318;
        }

        QPushButton#stop_btn { 
            background-color: #e35d6a; 
            color: white; 
            border-radius: 4px; 
            font-weight: bold; 
            padding: 5px 15px;
        }
        
        QPushButton#stop_btn:hover {
            background-color: #d14d5a;
        }

        /* Inputs */
        QLineEdit { 
            border: 1px solid #76ba1b; 
            border-radius: 3px; 
            padding: 4px; 
            background: white; 
            selection-background-color: #76ba1b;
        }

        /* Tables */
        QTableWidget { 
            background-color: white; 
            border: 1px solid #e0e0e0; 
            gridline-color: #f0f0f0; 
            outline: 0;
        }
        
        QHeaderView::section { 
            background-color: #76ba1b; 
            color: white; 
            padding: 5px; 
            border: 1px solid #68a318; 
            font-weight: bold; 
        }

        QTableWidget::item:selected {
            background-color: #f0f7e6;
            color: #333;
        }

        /* ScrollBars (Modern Thin Look) */
        QScrollBar:vertical {
            border: none;
            background: #f5f5f5;
            width: 10px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #ccc;
            min-height: 20px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #76ba1b;
        }
    """