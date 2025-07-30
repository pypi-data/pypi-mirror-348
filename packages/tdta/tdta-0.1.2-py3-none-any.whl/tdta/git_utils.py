import os
import zipfile

from tdta.command_line_utils import runcmd

GITHUB_SIZE_LIMIT = 100 * 1000 * 1000  # 100 MB


def add_new_files_to_git(project_folder, new_files):
    """
    Runs git add command to add imported files to the version control.
    Parameters:
        project_folder: project folder path
        new_files: imported/created file paths to add to the version control
    """
    for file_path in new_files:
        if os.path.getsize(file_path) > GITHUB_SIZE_LIMIT:
            zip_path = zip_file(file_path)
            new_files.remove(file_path)
            runcmd("cd {dir} && git add {zip_path}".format(dir=project_folder, zip_path=zip_path))
            runcmd("cd {dir} && git reset {file_path}".format(dir=project_folder, file_path=file_path))

    runcmd("cd {dir} && git add {files}".
           format(dir=project_folder,
                  files=" ".join([t.replace(project_folder, ".", 1) for t in new_files])))


def zip_file(file_path):
    """
    Zips the file if it exceeds the GitHub size limit.
    Parameters:
        file_path: file path to zip
    Returns: zipped file path
    """
    folder = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    zip_base = os.path.splitext(base_name)[0]

    single_zip_path = os.path.join(folder, f"{zip_base}.zip")
    with zipfile.ZipFile(single_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, base_name)

    return single_zip_path
