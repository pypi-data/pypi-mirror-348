import importlib
import os
import pathlib

__all__ = []  # This will collect all the names you want to expose

# Find all utility modules in this directory
_package_dir = pathlib.Path(__file__).parent

# for file in os.listdir(_package_dir):
#     if file.endswith(".py") and file != "__init__.py":
#         module_name = file[:-3]  # strip '.py'
#         module_path = f"{__name__}.{module_name}"
#         module = importlib.import_module(module_path)
#
#         # If the module defines __all__, expose those names at utils level
#         if hasattr(module, "__all__"):
#             for name in module.__all__:
#                 globals()[name] = getattr(module, name)
#                 __all__.append(name)