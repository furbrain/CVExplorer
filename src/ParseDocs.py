import os.path

import common
from functions.enum import Enum
from parser import ModuleParser

mod = ModuleParser().get_modules()
fname = common.get_config_filename("functions")
os.makedirs(os.path.dirname(fname), exist_ok=True)
print(f"saving data to {fname}")
with open(fname, "w") as f:
    mod.save(f)
fname = common.get_config_filename("enums")
with open(fname, "w") as f:
    Enum.save(f)
