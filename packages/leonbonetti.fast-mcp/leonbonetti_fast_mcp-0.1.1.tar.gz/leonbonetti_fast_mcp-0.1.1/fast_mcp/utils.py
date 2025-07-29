import os
import importlib
import inspect
from fast_mcp.structures.context import Context
from typing import List

def load_context_from_folder(folder_path: str) -> List[Context]:
    """
    Automatically load context files from the specified folder.
    This function will look for Python files in the folder and
    import all instances of Contexts inside the files.
    See in docs/contexts for more information.
    """
    # Implementation for loading context files goes here
    contexts = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_path = os.path.join(folder_path, filename)
            module_name = filename[:-3]

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Introspect all global variables and pick those that are instances of Context
            for _, obj in inspect.getmembers(module):
                if isinstance(obj, Context):
                    contexts.append(obj)
    return contexts