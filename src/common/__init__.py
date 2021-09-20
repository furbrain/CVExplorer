import appdirs
import os.path


def get_config_filename(name: str):
    return os.path.join(appdirs.user_config_dir("CVExplorer", "Underwood Underground"), f"{name}.json")
