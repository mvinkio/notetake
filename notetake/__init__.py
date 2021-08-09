import yaml
import os
import shutil
from pathlib import Path

import pandoc

PANDOC = pandoc
PANDOC.configure(auto=True)

NOTETAKE_DEFAULTS = Path(__file__).parent / 'config'

CONFIG_HOME = Path(os.environ['XDG_CONFIG_HOME']) / 'notetake'

shutil.rmtree(CONFIG_HOME)

CONFIG_HOME.mkdir(parents=True)
for yamlfile in NOTETAKE_DEFAULTS.glob('*.yaml'):
    dest = CONFIG_HOME / yamlfile.name
    shutil.copy(yamlfile, dest)

with open(CONFIG_HOME / 'config.yaml') as f:
    CONFIG = yaml.safe_load(f)

with open(CONFIG_HOME / 'metadata.yaml') as f:
    DEFAULT_PANDOC_METADATA = yaml.safe_load(f)
