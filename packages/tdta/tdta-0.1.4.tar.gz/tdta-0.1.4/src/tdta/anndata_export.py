
from pathlib import Path

from tdta.tdt_export import export_cas_data
from tdta.utils import read_project_config

from cas.anndata_conversion import merge
from cas.matrix_file.resolver import resolve_matrix_file_path


def export_anndata(sqlite_db: str, json_file: str, output_file: str, dataset_cache_folder: str = None):
    """
    Reads all data from TDT tables and generates CAS json.
    :param sqlite_db: db file path
    :param json_file: cas json file path
    :param output_file: output anndata path
    :param dataset_cache_folder: anndata cache folder path
    """
    project_config = read_project_config(Path(json_file).parent.absolute())
    if "matrix_file_id" in project_config:
        export_cas_data(sqlite_db, json_file, dataset_cache_folder)
        matrix_file_id = str(project_config["matrix_file_id"]).strip()
        anndata_path = resolve_matrix_file_path(matrix_file_id, dataset_cache_folder)

        merge(json_file, anndata_path, False, output_file)
