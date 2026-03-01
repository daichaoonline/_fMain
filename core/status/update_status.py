from dataclasses import dataclass
from typing import Optional
import logging

from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtWidgets import QTableWidget, QLabel, QTableWidgetItem


@dataclass
class DeviceUpdate:
    """Represents a single update to a device table cell."""
    col: int
    status: str
    extra: Optional[str] = None  # optional extra info


class UpdateStatus(QObject):
    # Signal now emits index and a list of DeviceUpdate objects
    update_row_signal = pyqtSignal(int, list)

    def __init__(self, tbl: QTableWidget, lbl: QLabel):
        super().__init__()
        self.tbl = tbl
        self.lbl = lbl
        self.index_to_row: dict[int, int] = {}

        self.lbl.setStyleSheet("font-weight: bold; font-size: 12px; font-family: Arial;")
        self.update_row_signal.connect(self.update_status)

    def update_status(self, index: Optional[int], updates: list[DeviceUpdate]):
        table = self.tbl

        # Reset table if index is None
        if index is None:
            table.setRowCount(0)
            self.index_to_row.clear()

        # Ensure row exists for given index
        if index is not None:
            row = self.index_to_row.get(index)
            if row is None:
                row = table.rowCount()
                table.insertRow(row)
                self.index_to_row[index] = row
            elif table.rowCount() <= row:
                table.insertRow(row)
        else:
            # Ensure enough rows exist for updates
            for i in range(len(updates)):
                if table.rowCount() <= i:
                    table.insertRow(table.rowCount())

        # Apply updates
        for i, update in enumerate(updates):
            if not isinstance(update, DeviceUpdate):
                logging.debug(f"Invalid update object at index {index}: {update}")
                continue

            item = QTableWidgetItem(str(update.status))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            target_row = row if index is not None else i
            table.setItem(target_row, update.col, item)

        # Number the first column
        for r in range(table.rowCount()):
            num_item = QTableWidgetItem(str(r + 1))
            num_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(r, 0, num_item)

        # Update label
        total_rows = table.rowCount()
        self.lbl.setText(f"{total_rows} Running...")
