from PyQt6 import QtWidgets
from dataclasses import dataclass
from widgets import (fmDevice, fmActive, fmAutoPost, fmManage, fmLogin)

@dataclass
class StackPage:
    stack: QtWidgets.QStackedWidget
    navDevice: QtWidgets.QPushButton
    navActive: QtWidgets.QPushButton
    navAutoPost: QtWidgets.QPushButton
    navManage: QtWidgets.QPushButton
    navLogin: QtWidgets.QPushButton
    
    def __post_init__(self):
        self.devicePages = QtWidgets.QWidget()
        self.activePages = QtWidgets.QWidget()
        self.autoPostPages = QtWidgets.QWidget()
        self.managePages = QtWidgets.QWidget()
        self.loginPages = QtWidgets.QWidget()
        
        self.dDevice = fmDevice()
        self.dDevice.setupUi(self.devicePages)
        self.stack.addWidget(self.devicePages)
        
        self.aActive = fmActive()
        self.aActive.setupUi(self.activePages)
        self.stack.addWidget(self.activePages)
        
        self.aPost = fmAutoPost()
        self.aPost.setupUi(self.autoPostPages)
        self.stack.addWidget(self.autoPostPages)
        
        self.mManage = fmManage()
        self.mManage.setupUi(self.managePages)
        self.stack.addWidget(self.managePages)
        
        self.lLogin = fmLogin()
        self.lLogin.setupUi(self.loginPages)
        self.stack.addWidget(self.loginPages)
        
        self.navMap = {
            self.navDevice: self.devicePages,
            self.navActive: self.activePages,
            self.navAutoPost: self.autoPostPages,
            self.navManage: self.managePages,
            self.navLogin: self.loginPages
        }
        
        for btn, page in self.navMap.items():
            btn.clicked.connect(lambda event, p=page: self.stack.setCurrentWidget(p))