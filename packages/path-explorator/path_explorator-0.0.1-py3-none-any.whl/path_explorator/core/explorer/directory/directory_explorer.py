from pathlib import Path
from src.path_explorator.exceptions import EntityDoesNotExists, NotADir
from src.path_explorator.core.explorer.path.path_creator import PathCreator

class DirectoryExplorer:
    def __init__(self, path_creator, root_dir_abs_path: str | Path):
        self.root_dir = self.__init_root_dir(root_dir_abs_path)
        self.path_creator: PathCreator = path_creator()

    def __init_root_dir(self, root_dir_abs_path: str | Path):
        if not isinstance(root_dir_abs_path, (str, Path)):
            raise TypeError(f'root_dir_abs_path type must be str or Path, not {type(root_dir_abs_path)}')
        root_dir = Path(root_dir_abs_path)

        if not root_dir.exists():
            raise EntityDoesNotExists(f'root directory does not exists at {root_dir}. Dir must exist')

        return root_dir

    def get_all_filenames_in_dir(self, dirpath: str | Path):
        path = Path(self.root_dir, dirpath)
        if not path.exists():
            raise EntityDoesNotExists(dirpath)
        if not path.is_dir():
            raise NotADir(dirpath)
        filenames = [fname for fname in path.iterdir() if fname.is_file()]
        return filenames

    def get_all_entitynames_in_dir(self, dirpath: str | Path):
        path = Path(self.root_dir, dirpath)
        if not path.exists():
            raise EntityDoesNotExists(dirpath)
        if not path.is_dir():
            raise NotADir(dirpath)
        entities_names = list(path.iterdir())
        return entities_names

    def is_exists(self, path:str | Path):
        entity = Path(path)
        return entity.exists()
    
    def is_file(self, path:str | Path):
        entity = Path(path)
        return entity.is_file()
        
    def is_dir(self, path:str | Path):
        entity = Path(path)
        return entity.is_dir()

    def find_file_path(self, searching_in, fname):
        searchable_dir = Path(self.root_dir, searching_in)
        return searchable_dir.rglob(fname)
    
    def get_name(self, path: str) -> str:
        if not isinstance(path, str):
            raise TypeError()
        entity_path = Path(path)
        return entity_path.name
        
    
    def join_with_rootdir(self, path):
        return f"{self.root_dir}/{path}"


