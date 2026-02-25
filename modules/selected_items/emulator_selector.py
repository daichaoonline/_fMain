from dataclasses import dataclass
from PyQt6.QtWidgets import QTableWidget, QLabel, QCheckBox
from typing import Optional
from thw_emulator import EmulatorManager

@dataclass
class SelectedItemsManager:
    alert_shown: bool = False
    total_item: list = None

    def __post_init__(self):
        if self.total_item is None:
            self.total_item = []

    def process_selection(self, tbl: QTableWidget):
        selected_index = set(item.row() for item in tbl.selectedItems())
        for row in selected_index:
            _emulator = 5556 + (row - 1) * 2
            index = f"emulator-{_emulator}"
            key = f"index-{row}"
            self.total_item.append({"row": row, "key": key, "D": index})
        return self.total_item
    
@dataclass
class EmulatorSelector:
    tbl: QTableWidget
    lbl: QLabel
    emulator: Optional[EmulatorManager] = None

    def _get_checkbox(self, row: int) -> QCheckBox | None:
        widget = self.tbl.cellWidget(row, 0)
        if not widget:
            return None
        return widget.findChild(QCheckBox)

    def sync_with_table_selection(self):
        selected_rows = {item.row() for item in self.tbl.selectedItems()}
        total_rows = self.tbl.rowCount()

        for row in range(1, total_rows):
            checkbox= self._get_checkbox(row)
            if checkbox:
                checkbox.setChecked(row in selected_rows)

        self.lbl.setText(f"Selected: {len(selected_rows)}")

    def select_valid_emulators(self):
        total_rows = self.tbl.rowCount()
        selected_count = 0

        for row in range(1, total_rows):
            index = row - 1
            if index >= len(self.emulator.ldplayer):
                continue

            name = self.emulator.ldplayer[index].name
            checkbox = self._get_checkbox(row)
            if not checkbox:
                continue

            is_valid = not name.endswith("$")
            checkbox.setChecked(is_valid)

            if is_valid:
                selected_count += 1

        self.lbl.setText(f"Selected: {selected_count}")

    def select_dollar_emulators(self):
        total_rows = self.tbl.rowCount()
        selected_count = 0

        for row in range(1, total_rows):
            index = row - 1
            if index >= len(self.emulator.ldplayer):
                continue

            name = self.emulator.ldplayer[index].name
            checkbox = self._get_checkbox(row)
            if not checkbox:
                continue

            has_dollar = name.endswith("$")
            checkbox.setChecked(has_dollar)

            if has_dollar:
                selected_count += 1

        self.lbl.setText(f"Selected: {selected_count} ($)")

    def select_running_emulators(self):
        total_rows = self.tbl.rowCount()
        selected_count = 0

        for row in range(1, total_rows):
            checkbox = self._get_checkbox(row)
            if not checkbox:
                continue

            status_item = self.tbl.item(row, 2)
            status = status_item.text() if status_item else ""

            is_running = status == "Running"
            checkbox.setChecked(is_running)

            if is_running:
                selected_count += 1

        self.lbl.setText(f"Selected: {selected_count} (Running)")
        
    def get_selected(self):
        return SelectedItemsManager().process_selection(self.tbl)