import os
from cas.file_utils import read_yaml_config


def read_project_config(root_folder_path):
    """
    Reads project configuration from the root folder and returns as dictionary.
    Params:
        root_folder_path: path of the project root folder.
    Returns: project configuration dictionary
    """
    for filename in os.listdir(root_folder_path):
        f = os.path.join(root_folder_path, filename)
        if os.path.isfile(f):
            if filename.endswith("_project_config.yaml"):
                return read_yaml_config(f)
