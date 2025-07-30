import os
import glob

from tdta.command_line_utils import runcmd


def git_update_local(project_folder: str, commit_message: str):
    """
    Composite git merge action to pull remote changes and merge them into the local branch. Instruct users about how to
    solve conflicts if they arise.
    :param project_folder: path to the project root folder
    :param commit_message: commit message for the merge action

    """
    print("Updating the project from the remote repository...")
    work_dir = os.path.abspath(project_folder)
    check_all_files_for_conflict(work_dir)
    current_branch = runcmd("cd {dir} && git branch --show-current".format(dir=work_dir), supress_logs=True).strip()
    if not current_branch:
        print("Git branch couldn't be identified in the project folder. Probably a previous rebase operation is in "
              "progress. Continuing the rebase operation.")
        runcmd("cd {dir} && git commit -a --message \"{msg}\"".format(dir=work_dir, msg=commit_message), supress_logs=True)
        runcmd("cd {dir} && git rebase --continue".format(dir=work_dir), supress_logs=True)
    try:
        runcmd("cd {dir} && git commit -a --message \"{msg}\"".format(dir=work_dir, msg=commit_message), supress_logs=True)
    except Exception as e:
        print("Error occurred during commit: " + str(e))

    pull_output = runcmd("cd {dir} && git pull --rebase=merges".format(dir=work_dir, branch=current_branch), supress_exceptions=True, supress_logs=True)
    if "CONFLICT" in pull_output:
        print("Conflicts occurred during the update process. Please resolve them manually and run the action again.")
        for message in pull_output.split("\n"):
            if "Merge conflict in" in message:
                print(">>>>  " + message)
        raise Exception("Conflicts occurred during the merge process. "
                        "Please resolve them manually and run the action again.")

    print("Project updated successfully.")


def check_all_files_for_conflict(work_dir: str):
    """
    Checks all files in the project folder for unresolved conflicts.
    """
    text_file_formats = ["json", "yml", "yaml", "txt", "md", "csv", "tsv", "html", "xml", "ts", "js", "py", "sh", "bat", "toml", "css"]
    managed_files_out = runcmd("cd {dir} && git ls-tree --full-tree --name-only -r HEAD".format(dir=work_dir),
                               supress_exceptions=True, supress_logs=True)
    managed_files = managed_files_out.split("\n")
    if not managed_files or len(managed_files) < 5:
        managed_files = get_all_files(work_dir)
    files_with_conflict = []
    for managed_file in managed_files:
        if managed_file.split(".")[-1] in text_file_formats:
            local_file = os.path.abspath(os.path.join(work_dir, managed_file))
            with open(local_file, 'r') as file:
                data = file.read()
                if "<<<<<<<" in data and "=======" in data:
                    files_with_conflict.append(local_file)

    for file in files_with_conflict:
        print(">>> Unresolved conflicts in file: " + file)
    if files_with_conflict:
        raise Exception("There are unresolved conflicts in the project. Please manually resolve them before continuing."
                        " See conflict handling instructions at https://brain-bican.github.io/"
                        "taxonomy-development-tools/Collaboration/ for more information.")


def get_all_files(work_dir: str):
    """
    Get all files in the project folder.
    :param work_dir: path to the project root folder
    :return: list of all files' path in the project folder relative to the work_dir
    """
    all_files = list()
    if not work_dir.endswith(os.sep):
        work_dir += os.sep
    for filename in glob.iglob(work_dir + '**/**', recursive=True):
        if not os.path.isdir(filename):
            all_files.append(os.path.relpath(filename, work_dir))
    return all_files
