from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QGroupBox)
from core import CheckLive

class CheckLiveUID(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Check Live UID")
        self.resize(900, 500)
        self.threads = []

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # --- UID input group ---
        group_uid = QGroupBox("UID Input")
        layout_uid = QVBoxLayout()
        self.textEdit_listUdid = QTextEdit()
        self.textEdit_listUdid.setPlaceholderText("Enter UIDs here...")
        layout_uid.addWidget(self.textEdit_listUdid)
        group_uid.setLayout(layout_uid)

        # --- Results group ---
        group_results = QGroupBox("Results")
        layout_results = QHBoxLayout()

        # Live Results group box
        group_live = QGroupBox("Live Results")
        layout_live = QVBoxLayout()
        self.textEdit_listCheckLive = QTextEdit()
        self.textEdit_listCheckLive.setPlaceholderText("Live Results")
        layout_live.addWidget(self.textEdit_listCheckLive)
        group_live.setLayout(layout_live)

        # Checkpoint Results group box
        group_checkpoint = QGroupBox("Checkpoint Results")
        layout_checkpoint = QVBoxLayout()
        self.textEdit_listCheckPoint = QTextEdit()
        self.textEdit_listCheckPoint.setPlaceholderText("Checkpoint Results")
        layout_checkpoint.addWidget(self.textEdit_listCheckPoint)
        group_checkpoint.setLayout(layout_checkpoint)

        # Add Live and Checkpoint groups to the Results layout
        layout_results.addWidget(group_live)
        layout_results.addWidget(group_checkpoint)
        group_results.setLayout(layout_results)

        # --- Buttons group ---
        group_buttons = QGroupBox("Actions")
        layout_buttons = QHBoxLayout()
        self.pushButton_checkLive = QPushButton("Check Live")
        self.pushButton_clearText = QPushButton("Clear")
        layout_buttons.addWidget(self.pushButton_checkLive)
        layout_buttons.addWidget(self.pushButton_clearText)
        group_buttons.setLayout(layout_buttons)

        # --- Totals group ---
        group_totals = QGroupBox("Totals")
        layout_totals = QHBoxLayout()
        self.label_totalCheckLive = QLabel("Total Live: 0")
        self.label_totalCheckPoint = QLabel("Total Checkpoint: 0")
        layout_totals.addWidget(self.label_totalCheckLive)
        layout_totals.addWidget(self.label_totalCheckPoint)
        group_totals.setLayout(layout_totals)

        # Add all groups to main layout
        main_layout.addWidget(group_uid)
        main_layout.addWidget(group_results)
        main_layout.addWidget(group_buttons)
        main_layout.addWidget(group_totals)

    def setup_connections(self):
        self.pushButton_checkLive.clicked.connect(self.check_live)
        self.pushButton_clearText.clicked.connect(self.clear_texts)
        self.textEdit_listUdid.textChanged.connect(self.auto_formart)

    def auto_formart(self):
        raw_text = self.textEdit_listUdid.toPlainText()
        uid_list = raw_text.splitlines()

        formatted_uids = []
        for uid in uid_list:
            parts = uid.strip().split("|")
            if parts and parts[0].strip():
                formatted_uids.append(parts[0].strip())

        self.textEdit_listUdid.blockSignals(True)
        self.textEdit_listUdid.setPlainText("\n".join(formatted_uids))
        self.textEdit_listUdid.blockSignals(False)

    def check_live(self):
        uids = self.textEdit_listUdid.toPlainText().splitlines()
        self.textEdit_listCheckLive.clear()
        self.textEdit_listCheckPoint.clear()
        self.label_totalCheckLive.setText("Total Live: 0")
        self.label_totalCheckPoint.setText("Total Checkpoint: 0")

        self.live_results = []
        self.checkpoint_results = []

        for uid in uids:
            uid = uid.strip()
            if not uid:
                continue
            thread = CheckLive(uid)
            thread.check_live.connect(self.update_results)
            thread.start()
            self.threads.append(thread)

    def update_results(self, uid, status):
        if status.lower() == "live":
            self.live_results.append(uid)
        else:
            self.checkpoint_results.append(uid)

        self.textEdit_listCheckLive.setPlainText("\n".join(self.live_results))
        self.textEdit_listCheckPoint.setPlainText("\n".join(self.checkpoint_results))
        self.label_totalCheckLive.setText(f"Total Live: {len(self.live_results)}")
        self.label_totalCheckPoint.setText(f"Total Checkpoint: {len(self.checkpoint_results)}")

    def clear_texts(self):
        self.textEdit_listUdid.clear()
        self.textEdit_listCheckLive.clear()
        self.textEdit_listCheckPoint.clear()
        self.label_totalCheckLive.setText("Total Live: 0")
        self.label_totalCheckPoint.setText("Total Checkpoint: 0")
        self.live_results = []
        self.checkpoint_results = []
        self.threads = []