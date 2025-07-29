from pathlib import Path
class DirectoryActor:

    def __init__(self, root_dir_abs_path: str):
        if not isinstance(root_dir_abs_path, str):
            raise TypeError(f'root_dir_abs_path argument must be str, not {type(root_dir_abs_path)}')
        self.root_dir = Path(root_dir_abs_path)
    def create_dir(self, path: str, name:str):
        """
        Creates directory/folder in specified path with specified name
        :param path: Path to the location of the future directory.
        The path must be relative to the root directory, which is passed as an argument to __init__ as root_dir_abs_path.
        This rule is used in every object where root_dir_abs_path is passed during initialization.
        :param name: name of dir
        :return: None
        """
        if not isinstance(path, str):
            raise TypeError(f'path argument must be str, not {type(path)}')
        if not isinstance(name, str):
            raise TypeError(f'name argument must be str, not {type(path)}')
        root_dir = Path(self.root_dir, path, name)
        root_dir.mkdir(exist_ok=True)

    def create_file(self, path: str, name: str):
        """
        Create file in specified path with specified name
        :param path: Path to the location of the future file.
        The path must be relative to the root directory, which is passed as an argument to __init__ as root_dir_abs_path.
        This rule is used in every object where root_dir_abs_path is passed during initialization.
        :param name: name of file
        :return: None
        """
        if not isinstance(path, str):
            raise TypeError(f'path argument must be str, not {type(path)}')
        if not isinstance(name, str):
            raise TypeError(f'name argument must be str, not {type(path)}')
        path_to_future_file = Path(self.root_dir, path, name)
        path_to_future_file.touch(exist_ok=True)