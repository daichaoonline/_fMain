class ColorButton:
    _TEMPLATE = """
    QPushButton {{
        background-color: {base};
        color: white;
        border: none;
        padding: 6px 12px;
    }}
    QPushButton:hover {{
        background-color: {hover};
    }}
    QPushButton:pressed {{
        background-color: {pressed};
    }}
    """

    @classmethod
    def _get_style(cls, base, hover, pressed):
        return cls._TEMPLATE.format(base=base, hover=hover, pressed=pressed)

    @staticmethod
    def blue():   return ColorButton._get_style("#0A4170", "#0C4C82", "#083455")
    
    @staticmethod
    def green():  return ColorButton._get_style("#4CAF50", "#45A049", "#3E8E41")
    
    @staticmethod
    def red():    return ColorButton._get_style("#F44336", "#D32F2F", "#B71C1C")
    
    @staticmethod
    def purple(): return ColorButton._get_style("#673AB7", "#5E35B1", "#512DA8")
    
    @staticmethod
    def orange(): return ColorButton._get_style("#FF9800", "#FB8C00", "#EF6C00")
    
    @staticmethod
    def dark():   return ColorButton._get_style("#1E1E1E", "#2C2C2C", "#151515")