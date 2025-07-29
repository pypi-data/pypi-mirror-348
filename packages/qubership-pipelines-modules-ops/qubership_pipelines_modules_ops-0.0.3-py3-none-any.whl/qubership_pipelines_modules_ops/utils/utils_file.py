import os
import yaml  # pip install pyyaml
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

try:
    from yaml import CSafeLoader as SafeLoader, CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeLoader, SafeDumper
logger.debug(f"Using {SafeLoader.__name__}, {SafeDumper.__name__} for yaml")

# https://stackoverflow.com/questions/45004464/yaml-dump-adding-unwanted-newlines-in-multiline-strings/45004775
yaml.add_representer(str,
        lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|' if '\n' in data else None),
        SafeDumper)


class UtilsFile:
    def write_file(content, file):
        if dirpath := Path(file).parent:
            dirpath.mkdir(parents=True, exist_ok=True)
        with open(file, 'w') as fs:
            fs.write(content)


class UtilsYaml:
    def read_yaml(file=None, /, string=None):
        if file:
            if isinstance(file, (str, bytes, os.PathLike,)):
                with open(file) as fs:
                    return yaml.load(fs, Loader=SafeLoader)
            else:  # stream
                return yaml.load(file, Loader=SafeLoader)
        return yaml.load(string, Loader=SafeLoader)

    def write_yaml(content, file=None, **kwargs):
        if not 'sort_keys' in kwargs:
            kwargs['sort_keys'] = False  # redefine default parameter value for yaml.dump()
        if file:
            if isinstance(file, (str, bytes, os.PathLike,)):
                filepath = Path(file)
                if dirpath := filepath.parent:
                    dirpath.mkdir(parents=True, exist_ok=True)
                with filepath.open('w') as fs:
                    yaml.dump(content, fs, Dumper=SafeDumper, **kwargs)
            else:  # stream
                yaml.dump(content, file, Dumper=SafeDumper, **kwargs)
        else:  # return str, as yaml.dump() does
            return yaml.dump(content, Dumper=SafeDumper, **kwargs)
