from pathlib import Path
from notetake import DEFAULT_PANDOC_METADATA, PANDOC_DEFAULTS, CONFIG_HOME
from notetake.utils import editor
from typing import List
import yaml
import re


class Collections:
    _collections = {}
    _active: Path = None

    def __init__(self, config):
        self._path: Path = Path(config['note_paths']['collections'])
        self.config: dict = config
        if 'collections' in self.config:
            self._active = Path(self.config['collections']['active'])

    def new(self, name):
        print("touching " + (self._path / name).as_posix())

        collection = self._path / name
        collection.mkdir(parents=True, exist_ok=True)

        self._collections[collection.name] = Collection(self.config, collection)

    def get_collections(self):
        for collection in self._path.glob('*'):
            self._collections[collection.name] = Collection(self.config, collection)
        return self._collections

    def edit(self, collection, module):
        collection: Collection = self._collections[collection]
        module: Module = collection.get_modules()[module]
        module.update_parts_view(module.get_parts().values())
        module.set_figures_in_metadata()
        self.set_active(module._root)
        editor([path.as_posix() for path in module.get_parts().values()])

    def add(self, collection: str, name: str):
        module = self._path / collection / name

        self.get_collections()
        if collection not in self._collections:
            print("collection doesn't exist")
            return False
        to_add_to: Collection = self._collections[collection]
        print("tyring to add name: " + name)
        print(to_add_to.get_modules())
        if name in to_add_to.get_modules():
            print('name is already taken')
            return False

        to_add_to.add(name, module)
        self.set_active(module)
        return True

    def set_active(self, module: Path):
        self._active = module

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.config.update({
            'collections': {
                'active': self._active.as_posix()
                }
            })
        self.write_config(CONFIG_HOME / 'config.yaml', self.config)

    def write_config(self, path, data, **kwargs):
        with open(path, 'w') as f:
            yaml.safe_dump(data, f, **kwargs)



class Collection:
    _modules = {}

    def __init__(self, config, path):
        self._path = path
        self.config = config

        self.metadata = self._path / 'collection_metadata.yaml'
        self.write_config(self.metadata, DEFAULT_PANDOC_METADATA, default_style="|")

        self._pandoc_options = self._path / 'pandoc_options.yaml'
        self.pandoc_options_data: dict = PANDOC_DEFAULTS
        self.pandoc_options_data['bibliography'] = self.config['bibliography']
        self.pandoc_options_data['metadata-files'] = [self.metadata.as_posix()]
        self.write_config(self._pandoc_options, self.pandoc_options_data)

    def write_config(self, path, data, **kwargs):
        with open(path, 'w') as f:
            yaml.safe_dump(data, f, **kwargs)

    def get_modules(self) -> dict:
        for module in [x for x in self._path.glob('*') if x.is_dir()]:
            self._modules[module.name] = Module(module, self.config, self.pandoc_options_data, DEFAULT_PANDOC_METADATA)
        return self._modules

    def add(self, name, path):
        self._modules[name] = Module(path, self.config, self.pandoc_options_data)


class Module:
    _parts = {}

    def __init__(self, path, config, pandoc_options, metadata):
        self.config = config
        self.pandoc_options = pandoc_options
        self.pandoc_metadata = metadata

        self._root = path
        self._parts_path = path / 'parts'
        self._figures = path / 'figures'

        if not self._parts_path.exists():
            self._parts_path.mkdir(parents=True)
        if not self._figures.exists():
            self._figures.mkdir(parents=True)

        parts = self.get_parts()

        if not parts:
            self.add_part()
            self.update_parts_view(self._parts.values())

    def update_parts_view(self, parts_paths: List[Path]):
        self.pandoc_options['input-files'] = [p.as_posix() for p in parts_paths]
        self.write_config(self._root.parent / 'pandoc_options.yaml', self.pandoc_options)

    def write_config(self, path, data, **kwargs):
        with open(path, 'w') as f:
            yaml.safe_dump(data, f, **kwargs)

    def add_part(self):
        parts = len(self.get_parts().keys())
        part: Path = self._root / 'parts' / str('part' + str(parts + 1) + '.md')
        part.touch()
        self._parts[part.name] = Path(part)

    def get_parts(self):
        for part in [x for x in self._parts_path.glob('*.md')]:
            self._parts[part.name] = part
        return self._parts

    def set_figures_in_metadata(self):
        header_string = self.pandoc_metadata['header-includes']
        header_string = re.sub(r"(\\newcommand{\\incfig[\s\S]*?\\import{).*?(}[\s\S]*)", r"\1" + self._figures.as_posix() + r"\2", header_string[0])
        self.pandoc_metadata['header-includes'] = [header_string]
        print(self.pandoc_metadata)
        print(self._root.parent)
        self.write_config(self._root.parent / 'collection_metadata.yaml', self.pandoc_metadata, default_style="|")

    def __str__(self):
        return "module{name=" + self._root.name + "}"

    def __repr__(self):
        return "module{name=" + self._root.name + "}"




class Part:
    ...
