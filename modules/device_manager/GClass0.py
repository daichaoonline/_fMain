from config import LDPlayerPathManager
from core.emulator import EmulatorPopulator
from thw_emulator import EmulatorManager

class GClass0(LDPlayerPathManager):
    """
    GClas0 manages LDPlayer emulator paths and provides
    an interface to the EmulatorManager.

    Attributes:
        ld_dir (str): Path to the LDPlayer installation directory.
        _emulator (EmulatorManager): Instance managing emulator operations.
    """

    def __init__(self) -> None:
        super().__init__()
        self.ld_dir: str = self.read_path()
        self._emulator: EmulatorManager = EmulatorManager(self.ld_dir)
        self._populator: EmulatorPopulator = EmulatorPopulator(self.ld_dir)

    def method_0(self) -> str:
        """
        Return the path to the LDPlayer installation directory.

        Returns:
            str: Path to the LDPlayer installation directory.
        
        """
        return self.ld_dir
    
    def method_1(self) -> EmulatorManager:
        """
        Return the EmulatorManager instance.

        Returns:
            EmulatorManager: The emulator manager object.
        """
        return self._emulator
    
    def method_2(self) -> EmulatorPopulator:
        """
        Return the EmulatorPopulator instance.

        Returns:

            EmulatorPopulator: The emulator populator object.
        """
        return self._populator
