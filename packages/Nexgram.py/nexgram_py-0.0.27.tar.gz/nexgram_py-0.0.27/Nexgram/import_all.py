import importlib
import os

def import_all(package_path):
  if not isinstance(package_path, str): return
  package_name = package_path.replace("/", ".")  
  package = importlib.import_module(package_name)
  folder_path = os.path.dirname(package.__file__)
  for file in os.listdir(folder_path):
    if file.endswith(".py") and file != "__init__.py":
      module_name = f"{package_name}.{file[:-3]}"
      importlib.import_module(module_name)