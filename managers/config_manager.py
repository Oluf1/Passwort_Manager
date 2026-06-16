import json


class ConfigManager:
    def __init__(self, path="config.json"):
        self.path = path
        self._config_data = None  # cache

    def load(self):
        with open(self.path, "r") as f:
            self._config_data = json.load(f)
        return self._config_data

    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
        self._config_data = data  # keep cache in sync

    @property
    def config(self):
        if self._config_data is None:
            self._config_data = self.load()

        assert self._config_data is not None
        return self._config_data["config"]
        

    @property
    def theme_name(self):
        return self.config["theme"]

    @property
    def font_family(self):
        return self.config["font_family"]
    @property
    def items_per_page(self):
        return self.config["items_per_page"]
    @property
    def default_kdf(self):
        return self.config["Kdf_type"]