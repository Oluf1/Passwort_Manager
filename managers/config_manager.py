import json
from typing import List

class ConfigManager:
    def __init__(self, path="config.json"):
        self.path = path
        self.load()  # cache

    def load(self):
        with open(self.path, "r") as f:
            self._config_data = json.load(f)
        return self._config_data

    def save(self):
        assert self._config_data is not None
        data = self._config_data
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
        self._config_data = data  # keep cache in sync

    @property
    def config(self):
        if self._config_data is None:
            self._config_data = self.load()

        assert self._config_data is not None
        return self._config_data
        

    @property
    def theme_name(self):
        return self.config["theme"]

    @theme_name.setter
    def theme_name(self, value):
        self.config["theme"] = value


    @property
    def font_family(self):
        return self.config["font_family"]

    @font_family.setter
    def font_family(self, value):
        self.config["font_family"] = value


    @property
    def items_per_page(self):
        return self.config["items_per_page"]

    @items_per_page.setter
    def items_per_page(self, value):
        self.config["items_per_page"] = value

    @property
    def supported_kdfs(self)->List[str]:    
        return ["Argon2", "PBKDF2"]
        
    @property
    def default_kdf(self):
        return self.config["Kdf_type"]

    @default_kdf.setter
    def default_kdf(self, value):
        self.config["Kdf_type"] = value