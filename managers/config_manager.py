import json


class ConfigManager:
    def __init__(self, path="config.json"):
        self.path = path

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    @property
    def config(self):
        return self.load()["config"]

    @property
    def vaults(self):
        return self.load()["Vaults"]