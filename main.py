from package import *

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class MainWindow(QMainWindow, fmHFarm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(1100, 590)
        self.meta = AppMeta()
        self.services = CoreServices()
        
        self.selectors = []
        self.emulator = []

        self.main = StackPage(
            self.stackWidget,
            navDevice=self.btnDevices,
            navActive=self.btnActive,
            navAutoPost=self.btnAutoPost,
            navManage=self.btnManage,
            navLogin=self.btnLogin
        )
        
        self.dDevice = self.main.dDevice
        self.aActive = self.main.aActive
        self.aPost = self.main.aPost
        self.mManage = self.main.mManage
        self.lLogin = self.main.lLogin

        # Navigation
        self._navigation()
        self._standard_pixmap()
        self.menu_bar()
        self._check_license()
        self.signal_connect()

        # Theme selector
        self.themeSelector = ThemeSelector(self, '')
        self.vbTbl.addWidget(self.themeSelector.build_widget())

        self.tbl = [
            self.aActive.tblEmulator,
            self.aPost.tblEmulator,
            self.mManage.tblEmulator,
            self.lLogin.tblEmulator
        ]
        
        for tb in self.tbl:
            TableConfigurator(tb)
        
        self.lbl = [
            self.aActive.lblSelected,
            self.aPost.lblSelected,
            self.mManage.lblSelected,
            self.lLogin.lblSelected
        ]

        for table, label in zip(self.tbl, self.lbl):
            self.selector = EmulatorSelector(table, label)
            table.itemSelectionChanged.connect(self.selector.sync_with_table_selection)
            self.selectors.append(self.selector)  
            
        self._load_emulator()

    def signal_connect(self):
        self.dDevice.btnRefreshPath.clicked.connect(self._load_emulator)

    def _load_emulator(self):
        start_time = time.time()
        self.grbTop.setTitle("Loading... (0%)")

        self.load_path = LDPlayerPathManager().read_path()
        self.dDevice.txtLdPath.setText(
            self.load_path
            if self.load_path
            and os.path.exists(
                self.load_path
            )
            else ""
        )

        self.threads = EmulatorPopulator(self.load_path)

        def update_progress(percent):
            elapsed = int(time.time() - start_time)
            minutes, seconds = divmod(elapsed, 60)
            self.grbTop.setTitle(f"Loading... ({percent}%)  [{minutes:02d}:{seconds:02d}]")
        
        self.threads.progress_signal.connect(update_progress)
        self.threads.emulator_signal.connect(self.update_emulator_table)

        def finished(total):
            for label in self.lbl:
                label.setText(f"Total: {total}")
            self.grbTop.setTitle("System ready!")
            
        self.threads.finished_signal.connect(finished)
        self.threads.start()
            
    def update_emulator_table(self, index):
        em = index["em"]
        for tbl in self.tbl:
            tbl.setUpdatesEnabled(False)
            
            _row = tbl.rowCount()
            tbl.insertRow(_row)

            checkbox = QCheckBox()
            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            tbl.setCellWidget(_row, 0, cell_widget)

            name_item = QTableWidgetItem(str(em.name))
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tbl.setItem(_row, 1, name_item)

            tbl.setUpdatesEnabled(True)
                                                                    
    def _navigation(self):
        self.btnDevices.setStyleSheet(ColorButton.blue())
        self.btnActive.setStyleSheet(ColorButton.green())
        self.btnAutoPost.setStyleSheet(ColorButton.red())
        self.btnManage.setStyleSheet(ColorButton.purple())
        self.btnLogin.setStyleSheet(ColorButton.dark())

    def _standard_pixmap(self):
        self.btnStart.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; }"
        )
        self.btnStart.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPlay
            )
        )

        self.btnStop.setStyleSheet(
            "QPushButton { background-color: #f44336; color: white; }"
        )
        self.btnStop.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaStop
            )
        )
        
        self.btnReload.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }"
        )
        
        self.btnReload.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_BrowserReload
            )
        )

    def _check_license(self):    
        if self.services.license_service.validate_local_license():
            return

        dialog = RegisterForm(self.services.license_service, self.services.telegram_notifier)
        dialog.exec()

        if not self.services.license_service.validate_local_license():
            QMessageBox.critical(self, "Error", "License is required to use this app.")
            sys.exit()
            
    def menu_bar(self):
        self.actionReport_Issue.triggered.connect(self.handle_report_issue)
        self.actionCheck_for_Updates.triggered.connect(self.handle_check_updates)
        self.actionAbout.triggered.connect(self.show_about_dialog)
        self.actionQuit.triggered.connect(self.confirm_quit)

    def confirm_quit(self):
        reply = QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to quit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            
    def handle_report_issue(self):
        report = ReportIssues(
            bot_token=self.services.env["bot_token"],
            chat_id=self.services.env["chat_id"],
            parent=self
        )
        report.report()

    def handle_check_updates(self):
        updater = CheckUpdates(
            current_version=self.meta.__version__,
            json_url=self.services.env["url"],
            parent=self
        )
        updater.check_for_updates()    
                
    def show_about_dialog(self):       
        expiry = self.services.license_service.get_online_expiry_date()
        dialog = AboutDialog(
            title=self.meta.__title__,
            expiry_date=expiry,
            version=self.meta.__version__,
            developer=self.meta.__developer__,
            copyright=self.meta.__copyright__,
            parent=self
        )
        dialog.exec()


if __name__ == "__main__":
    meta = AppMeta()
    app = QApplication(sys.argv)
    app.setStyleSheet(LoadStylesheet("light").content)
    app.setWindowIcon(QIcon(meta.__icon__))
    main = AppSplashScreen()
    main.start()
    sys.exit(app.exec())