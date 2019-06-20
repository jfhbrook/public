_CONFIG = dict(
    timeout=(int, 60, {'INFINITY': 2**31})
)


class ConfigError(Exception):
    pass


class Config:
    def __init__(self):
        self._reset()

    def _reset(self):
        for key, (type_, default, sentinels) in _CONFIG.items():
            setattr(self, key, default)

    def reset(self):
        self._reset()
        self.show()

    def _check_is_in(self, key):
        if key not in _CONFIG:
            raise ConfigError("Unknown configuration option '{}'".format(key))

    def set(self, key, raw_value):
        self._check_is_in(key)

        type_, default, sentinels = _CONFIG[key]

        if raw_value in sentinels:
            value = sentinels[raw_value]
        else:
            value = type_(raw_value)

        setattr(self, key, value)
        self.show(key)

    def get(self, key):
        self._check_is_in(key)
        return getattr(self, key)

    def show(self, key=None):
        if key is None:
            for k in _CONFIG.keys():
                self.show(k)
        else:
            print('{}={}'.format(key, self.get(key)))


config = Config()
