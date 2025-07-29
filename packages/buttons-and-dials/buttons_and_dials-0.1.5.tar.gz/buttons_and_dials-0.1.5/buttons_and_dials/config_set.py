from os import getenv
from pathlib import Path
import sys
try:
    import tomllib
except:
    import tomli as tomllib

def safe_open_toml(path):
    if Path(path).is_file():
        with open(path, "rb") as f:
            return tomllib.load(f)
    else:
        print(f"File {path} does not exist")
        sys.exit(1)


class ConfigSet:
    def __init__(self, set_name, initial_settings_path, check_cwd=True,
                 argv_prefix=None):
        self._initial_settings_path = initial_settings_path
        if set_name.endswith('.toml'):
            self._set_name = set_name[:-4]
        else:
            self._set_name = set_name
        self._settings = self._load_settings(check_cwd)
        if argv_prefix:
            argsdict = self._settings_from_argv(argv_prefix)
            self._settings.update(argsdict)

    def __getattribute__(self, name: str):
        if name.startswith('_'):
            return super().__getattribute__(name)

        elif name in self._settings:
            return self._settings[name]

        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {name}")

    def _load_settings(self, check_cwd):
        # Load default settings first
        settings_dict = safe_open_toml(self._initial_settings_path)

        if check_cwd:
            cwd = Path.cwd()
            cwd_l = cwd / f"{self._set_name}.toml"
            if cwd_l.exists() and cwd_l.is_file():
                settings_dict.update(safe_open_toml(cwd_l))

        # Finally, if there is an environment variable {set_name}_FILE, load it
        if env_path := getenv(f"{self._set_name}_FILE"):
            settings_dict.update(safe_open_toml(env_path))
        return settings_dict

    def _settings_from_argv(self, argv_prefix):
        if not argv_prefix.endswith('='):
            argv_prefix += '='
        args = [a[len(argv_prefix):] for a in sys.argv[1:] if a.startswith(argv_prefix)]
        argsdict = {}
        for arg in args:
            if '=' not in arg:
                print(f'Invalid arg {arg}, missing "="')
                continue
            k, v = arg.split('=')
            if k in argsdict:
                if not isinstance(argsdict[k], list):
                    argsdict[k] = [argsdict[k]]
                argsdict[k].append(v)
            else:
                argsdict[k] = v
        # Lets make toml parse data types
        string = ''
        for k, v in argsdict.items():
            string += f"{k} = {v}\n"
        return tomllib.loads(string)
