from conippets import json

class Config(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = Config(**v)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError(f"'Config' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        self[name] = value

    @staticmethod
    def from_json(file):
        cfg = json.read(file)
        if not isinstance(cfg, dict):
            raise RuntimeError("Only 'dict' object is supported!")
        return Config(**cfg)

    def save(self, file):
        json.write(file, self)