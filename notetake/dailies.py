from notetake import PANDOC
from pathlib import Path
from typing import List

from pandoc.types import Pandoc

class Dailies:

    def __init__(self, config):
        self.dailies_dir = Path(config['note_paths']['dailies'])
        self.figures_dir = self.dailies_dir / 'figures'

        print("Making dailies collection")
        print(self.dailies_dir)
        print(self.figures_dir.absolute())

        self._dailies: List[Daily] = []
        print("finding dailies in: " + str(self.dailies_dir.absolute()))
        for daily_path in self.dailies_dir.glob('*.md'):
            self._dailies.append(Daily(daily_path))

    def __enter__(self):
        ...

    def __exit__(self, type, value, traceback):
        ...


class Daily:
    def __init__(self, daily_path: Path):
        ...
