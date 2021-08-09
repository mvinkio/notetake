from pathlib import Path
from notetake import DEFAULT_PANDOC_METADATA, PANDOC_DEFAULTS
from notetake.utils import editor
from typing import List
import yaml


class Collections:
    _collections = {}

    def __init__(self, config):
        self._path: Path = Path(config['note_paths']['collections'])
        self.config = config

    def new(self, name):
        print("touching " + (self._path / name).as_posix())

        collection = self._path / name
        collection.mkdir(parents=True, exist_ok=True)

        self._collections[collection.name] = Collection(self.config, collection)

    def get_collections(self):
        for collection in self._path.glob('*'):
            self._collections[collection.name] = Collection(self.config, collection)

    def add(self, collection: Path, name: str):
        self.get_collections()
        if collection.name not in self._collections:
            return False
        to_add_to = self._collections[collection.name]
        if name in to_add_to.get_modules():
            print('name is already taken')
            return False

        parts = collection / name / 'parts'
        parts.mkdir(parents=True)

        figures = collection / name / 'figures'
        figures.mkdir(parents=True)

        to_add_to.add(name, Module(collection / name, to_add_to))
        return True

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        ...


class Collection:
    _modules = {}

    def __init__(self, config, path):
        self._path = path
        self.config = config

        self._pandoc_options = self._path / 'pandoc_options.yaml'

        self.pandoc_options_data: dict = PANDOC_DEFAULTS
        self.pandoc_options_data['bibliography'] = self.config['bibliography']

        metadata = self._path / 'collection_metadata.yaml'
        self.write_config(metadata, DEFAULT_PANDOC_METADATA, default_style="|")
        self.write_config(self._pandoc_options, self.pandoc_options_data)

    def update_parts_view(self, parts_paths: List[Path]):
        self.pandoc_options_data['input-files'] = [p.as_posix() for p in parts_paths]
        self.write_config(self._pandoc_options, self.pandoc_options_data)

    def write_config(self, path, data, **kwargs):
        with open(path, 'w') as f:
            yaml.safe_dump(data, f, **kwargs)

    def get_modules(self) -> dict:
        return self._modules

    def add(self, name, module):
        self._modules[name] = module


class Module:
    def __init__(self, path, collection):
        self.collection = collection
        self._root = path
        self._parts_paths = list(path.glob('parts/*.md'))
        if len(self._parts_paths) == 0:
            self.add_part()
            collection.update_parts_view(self._parts_paths)

    def add_part(self):
        parts = len(self._parts_paths)
        part: Path = self._root / 'parts' / str('part' + str(parts + 1) + '.md')
        part.touch()
        self._parts_paths.append(part)


class Part:
    ...
