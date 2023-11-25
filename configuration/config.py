import json
from pathlib import Path


def load_config():
    settings_file = Path.cwd() / "configuration" / 'settings.json'

    if Path(settings_file).exists():
        with open(settings_file, 'r') as json_file:
            conf = json.load(json_file)
        return conf
    else:
        return False
   


