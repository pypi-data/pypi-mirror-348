from pathlib import Path
from typing import Union, List
class DirectoryActor:

    def create_dir(self, path: Union[str, Path], name:str):
        root_dir = Path(path) if isinstance(path, str) else path
        root_dir.mkdir(exist_ok=True)

    def create_file(self, path, name):
        path_to_future_file = Path(path / name)
        path_to_future_file.touch(exist_ok=True)