import os
import importlib

def load_all_rules():
    current_dir = os.path.dirname(__file__)
    for filename in os.listdir(current_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"syspect.rules.{filename[:-3]}"
            importlib.import_module(module_name)

# Automatically load all rules when this package is imported
load_all_rules()
