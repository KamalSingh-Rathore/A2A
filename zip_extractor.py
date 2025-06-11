import zipfile
from tempfile import TemporaryDirectory
from pathlib import Path
from typing import List



def traverse_directory(path: Path, level=0, base_path=None, skip_files=List[str],skip_directory=List[str]):
    """
    Traverse the directory and print all files and directories in a tree format.
    """
    if base_path is None:
        base_path = path

    indent = "    " * level
    prefix = "|--" if level > 0 else ""

    for item in sorted(path.iterdir()):
        if item.name.startswith('.'):
            continue  # Skip hidden files/folders

        relative_path = item.relative_to(base_path)

        with open('structure.txt', 'a') as f:
            f.write(f"{indent}{prefix} {relative_path}\n")
            f.close()

        import chardet

        if item.is_file()  and item.name not in skip_files:
            with open(item.absolute(), 'rb') as file_in, open('content.txt', 'a') as file_out:
                data = file_in.read()
                file_out.write(f"\n \n Content of file {relative_path}:\n \n \n \n  {data} \n \n Content ends of file {relative_path} {'-'*40}\n")
                file_out.close()
                file_in.read()


        if item.is_dir():
            if item.name not in skip_directory:
                traverse_directory(item, level + 1, base_path)


def zip_extractor(repo_url, extract_to="./repo",skip_files=List[str],skip_directory=List[str]):
    with zipfile.ZipFile(repo_url, 'r') as f :
        with TemporaryDirectory(delete=False) as tmpdir:
            f.extractall(tmpdir)

        pa = Path(tmpdir)

        traverse_directory(path=pa,skip_files=skip_files,skip_directory=skip_directory)







