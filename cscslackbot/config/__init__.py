import yaml


def dict_merge(merged, source, overwrite=False):
    for k in source.keys():
        if k not in merged:
            merged[k] = source[k]
        elif isinstance(merged[k], dict) and isinstance(source[k], dict):
            dict_merge(merged[k], source[k], overwrite=overwrite)
        elif overwrite:
            merged[k] = source[k]


class Configuration(dict):
    def __init__(self, config_file=None, defaults_file=None, secrets_file=None):
        super(dict, self).__init__()
        if config_file:
            self.load(config_file, defaults_file)
        if secrets_file:
            self.load_secrets(secrets_file)

    def get(self, entry, default=None):
        path = entry.split('/')
        entry = self
        try:
            for elem in path:
                entry = entry[elem]
        except KeyError:
            return default

        return entry

    def put(self, entry, value):
        path = entry.split('/')
        path = path[:-1]
        key = path[-1]
        root = self
        for elem in path:
            if elem not in root:
                root[elem] = {}
            root = root[elem]

        root[key] = value

    def load(self, config_file, defaults_file=None, section=None):
        self.load_defaults(defaults_file=defaults_file, section=section)

        open(config_file, 'a').close()
        with open(config_file, 'r') as f:
            loaded = yaml.safe_load(f)

        if not loaded:
            loaded = {}

        if section is None:
            dict_merge(self, loaded, overwrite=True)
        elif section in self:
            dict_merge(self[section], loaded, overwrite=True)
        else:
            self[section] = loaded

    def load_defaults(self, defaults_file=None, section=None):
        if defaults_file is None:
            # Create an empty configuration section
            loaded = {}
        else:
            # Create a config section using the spec file
            with open(defaults_file, 'r') as f:
                loaded = yaml.safe_load(f)

        if section is None:
            # Merge into base config
            dict_merge(self, loaded, overwrite=False)
        elif section in self:
            dict_merge(self[section], loaded, overwrite=False)
        else:
            self[section] = loaded

    def load_secrets(self, secrets_file):
        self.load(secrets_file, section='secrets')
