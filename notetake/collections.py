from pathlib import Path
from notetake import DEFAULT_PANDOC_METADATA
import yaml


class Collections:
    def __init__(self, config):
        self._path = Path(config['note_paths']['collections'])

    def new(self, name):
        print("touching " + (self._path / name).as_posix())

        collection = self._path / name
        collection.mkdir(parents=True, exist_ok=True)

        collection_metadata = collection / 'collection_metadata.yaml'
        print(DEFAULT_PANDOC_METADATA['header-includes'])
        with open(collection_metadata, 'w') as f:
            yaml.safe_dump(DEFAULT_PANDOC_METADATA, f, default_style="|")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        ...
