from PyQt6.QtWidgets import (
    QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QLineEdit,
    QTextEdit, QComboBox, QTimeEdit, QDateEdit
)

class GClass2:
    @staticmethod
    def getSpinBox(spinbox: QSpinBox):
        return spinbox.value() if spinbox else 0

    @staticmethod
    def getDoubleSpinBox(double_spinbox: QDoubleSpinBox):
        return double_spinbox.value() if double_spinbox else 0.0

    @staticmethod
    def getCheckBox(checkbox: QCheckBox):
        return checkbox.isChecked() if checkbox else False

    @staticmethod
    def getRadioButton(radio_button: QRadioButton):
        return radio_button.isChecked() if radio_button else False

    @staticmethod
    def getText(line_edit: QLineEdit):
        return line_edit.text().strip() if line_edit else ""

    @staticmethod
    def getPlainText(text_edit: QTextEdit):
        return text_edit.toPlainText().strip() if text_edit else ""

    @staticmethod
    def getComboBox(combo_box: QComboBox):
        return combo_box.currentText().strip() if combo_box else ""

    @staticmethod
    def getTime(time_edit: QTimeEdit):
        if time_edit:
            return time_edit.time().toString("HH:mm:ss")
        return ""

    @staticmethod
    def getDate(date_edit: QDateEdit):
        if date_edit:
            return date_edit.date().toString("yyyy-MM-dd")
        return ""