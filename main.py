from core.status.update_status import DeviceUpdate
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
        self.running_threads = []
        
        self.stop_running_task = threading.Event()
        self.pause_running_task = threading.Event()
        
        self.func = GClass0()

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
            table.itemSelectionChanged.connect(
                self.selector.sync_with_table_selection
            )
            self.selectors.append(self.selector)  
            
        self._load_emulator()

    def signal_connect(self):
        self.dDevice.btnReloadPath.clicked.connect(self._load_emulator)
        self.btnStart.clicked.connect(self.start_emulators)

    def _load_emulator(self):
        start_time = time.time()
        self.grbTop.setTitle("Loading... (0%)")

        self.load_path = self.func.method_0()
        self.dDevice.txtLdPath.setText(
            self.load_path
            if self.load_path
            and os.path.exists(
                self.load_path
            )
            else ""
        )

        self.threads = self.func.method_2()
        self.threads.start()
        self.emulator = self.func.method_1()
        
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

    def start_emulators(self):
        self.snapshot = GEnum0(
            self.dDevice,
            self.aActive,
            self.aPost,
            self.mManage,
            self.lLogin
        )
        
        self.method_109 = self.snapshot.method_77()

        nudRunThread = self.method_109['nudRunThread']
        nudMaxThread = self.method_109['nudMaxThread']
        nubWaitAfter = self.method_109['nubWaitAfter']
        nubBetweenLoop = self.method_109['nubBetweenLoop']
        
        # In MainWindow.start_emulators
        self.update_status = UpdateStatus(
            self.tblStatus,
            self.dDevice.lblRunThread
        )
        
        def worker_thread():
            try:
                selected_indices = []
                for table in self.tbl:
                    for row in range(table.rowCount()):
                        widget = table.cellWidget(row, 0)
                        if widget:
                            checkbox: QCheckBox = widget.findChild(QCheckBox)
                            if checkbox and checkbox.isChecked():
                                selected_indices.append(row)

                if not selected_indices:
                    print("No devices selected")
                    return

                self.tblStatus.setRowCount(0)
                self.update_status.index_to_row = {em_index: pos for pos, em_index in enumerate(selected_indices)}
                to_start = selected_indices[:nudMaxThread]
                
                with ThreadPoolExecutor(max_workers=nudRunThread) as executor:
                    futures = {}
                    for index in to_start:
                        if self.stop_running_task.is_set():
                            logging.debug("Stop signal received before starting index %s", index)
                            break

                        while self.pause_running_task.is_set():
                            if self.stop_running_task.is_set():
                                logging.debug("Stop signal received during optimizer pause")
                                return
                            sleep(0.5)        
                            
                        if self.stop_running_task.is_set():
                            logging.debug("Stop signal received before submitting index %s", index)
                            break
                    
                        future = executor.submit(self.manage_emulator_safe, index, nubWaitAfter)
                        futures[future] = index
                        sleep(nubBetweenLoop)
            
                    for future in as_completed(futures):
                        if self.stop_running_task.is_set():
                            logging.debug("Stop signal received while waiting for futures")
                            break                        
                        try:
                            future.result()
                        except Exception as e:
                            logging.debug(f"Unhandled error in index {futures[future]}: {e}")

            except Exception as e:
                logging.critical(f"Application crash in worker_thread thread: {e}", exc_info=True)
                            
        self.worker_thread = threading.Thread(target=worker_thread, daemon=True)
        self.worker_thread.start()

    def manage_emulator_safe(self, index, wait_time):
        try:
            max_retries = 2
            retry_count = 0
            process_close = 10
            
            recoverable_errors = (
                "Failed to open Facebook app", "Video import failed",
                "Failed to get profile", "Not Connecting...", "Failed connecting...",
                "ip", "Failed: Switch Profile")
            
            try:
                while retry_count < max_retries:
                    self.update_status.update_row_signal.emit(index, [ DeviceUpdate(col=2, status=f"Processing {retry_count + 1}/{max_retries}")])
                    if self.stop_running_task.is_set():
                        return

                    if index not in self.running_threads:
                        self.running_threads.append(index)
                        
                    try:
                        self.emulator.launch_instance(index)
                        self.emulator.organize_windows()

                        sleep(wait_time)
                                
                        sleep(process_close)
                        self.emulator.stop_instance(index)
                        return

                    except Exception as einner:
                        message = str(einner)
                        logging.debug(f"[ERROR] index={index}, attempt={retry_count+1}, error={message}")
                        if any(x in message for x in ["Failed connecting...", "Not Connecting...", "ip"]): 
                            self.emulator.stop_instance(index)
                            logging.debug(f"[CLOSED] Emulator closed due to 'Failed connecting...' index={index}")
                            retry_count += 1
                            sleep(process_close)
                            continue
                                                
                        elif any(error in message for error in recoverable_errors):
                            retry_count += 1
                            logging.debug(f"[RETRY] index={index}, retry_count={retry_count}")
                            sleep(process_close)
                            continue
                        
                        else:
                            logging.debug(f"[FATAL] index={index}, error={message}")
                            continue
                            
                if retry_count >= max_retries:
                    self.update_status.update_row_signal.emit(index, [(3, f"Disconnected {index}")])

            finally:
                sleep(process_close)
                self.update_status.update_row_signal.emit(index, [(3, f"Close: {process_close}")])
                self.emulator.stop_instance(index)
                
                if index in self.running_threads:
                    self.running_threads.remove(index)
                    
                # self.update_status.remove_row_signal.emit(index)
                
        except Exception as e:
            logging.error(f"[THREAD ERROR] index={index}, error={e}\n{traceback.format_exc()}")
            self.update_status.update_row_signal.emit(em_index=index, updates=[(3, f"Crash: {str(e)[:50]}...")])
                
            try:
                self.emulator.stop_instance(index)
            except Exception as e:
                logging.error(f"[THREAD ERROR] index={index}, error={e}\n{traceback.format_exc()}")
            
            return

                        
if __name__ == "__main__":
    meta = AppMeta()
    app = QApplication(sys.argv)
    app.setStyleSheet(LoadStylesheet("light").content)
    app.setWindowIcon(QIcon(meta.__icon__))
    main = AppSplashScreen()
    main.start()
    sys.exit(app.exec())