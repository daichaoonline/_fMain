from dataclasses import dataclass, asdict
import random
from copy import deepcopy
from .GClass2 import *
from widgets import (
    fmDevice,
    fmActive,
    fmAutoPost,
    fmManage,
    fmLogin
)

@dataclass
class DeviceActions:
    nudMaxThread: QSpinBox
    nubBetweenLoop: QSpinBox
    nubWaitAfter: QSpinBox
    nudMaxRetries: QSpinBox
    nudCloseBeforeTo: QCheckBox
    nudCloseBeforeFrom: QSpinBox
    nudRunThread: QSpinBox

class GEnum0(GClass2):
    def __init__(
        self,
        dDevice: fmDevice,
        aActive: fmActive,
        aPost: fmAutoPost,
        mManage: fmManage,
        lLogin: fmLogin
    ) -> None:
        super().__init__()
        
        self.dDevice = dDevice
        self.aActive = aActive
        self.aPost = aPost
        self.mManage = mManage
        self.lLogin = lLogin
        
        self.device_action = None
        self.action_snapshot = []
        self.method_76()
    
    def method_76(self):
        self.device_action = DeviceActions(
            self.getSpinBox(self.dDevice.nudMaxThread),
            self.getSpinBox(self.dDevice.nubBetweenLoop),
            self.getSpinBox(self.dDevice.nubWaitAfter),
            self.getSpinBox(self.dDevice.nudMaxRetries),
            self.getSpinBox(self.dDevice.nudCloseBeforeTo),
            self.getSpinBox(self.dDevice.nudCloseBeforeFrom),
            self.getSpinBox(self.dDevice.nudRunThread)
        )
        self.device_action = deepcopy(self.device_action)

    def method_77(self):
        action_dict = asdict(self.device_action)
        enabled_actions = [key for key, val in action_dict.items() if val]
        random.shuffle(enabled_actions)
        self.action_snapshot = enabled_actions 
        
        return action_dict