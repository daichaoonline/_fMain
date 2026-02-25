import os
import json

class LDPlayerPathManager:
    """Manage the LDPlayer installation path stored in a JSON config file."""

    def __init__(self):
        appdata = os.getenv("APPDATA")
        self.config_file = os.path.join(appdata, "ldplayer.json")

    def read_path(self) -> str:
        """Return the saved LDPlayer path, or empty string if not set."""
        if not os.path.exists(self.config_file):
            return ""

        with open(self.config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["ld_path"]

    def write_path(self, path: str):
        """Save the LDPlayer path to the config file."""
        data = {"ld_path": path}
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)