from pathlib import Path
import json
import binascii
import os
from dataclasses import dataclass

@dataclass
class Vault:
    name:str
    vault_type: str
    key_path: Path
    data_path: Path
class VaultManager:
    def __init__(self, vaults_file="vaults.json"):
        self.config_file = vaults_file
        self.vaults = {}
        self.load_vaults()

    def load_vaults(self):
        with open(self.config_file, "r") as file:
            data = json.load(file)

        for name in data:
            vault_type = data["type"]
            key_path = data["directories"][0]
            data_path = data["directories"][1]
            
            self.vaults[name] = Vault(name,vault_type,key_path,data_path)

    def save_vaults(self):
        with open(self.config_file, "r") as file:
            data = json.load(file)

        data = self.vaults

        with open(self.config_file, "w") as file:
            json.dump(data, file, indent=2)

    def get_vault_names(self):
        return list(self.vaults.keys())

    def get_vault(self, name):
        return self.vaults.get(name)

    def create_vault(self, name, key_path, data_path):
        if name in self.vaults:
            raise ValueError("Vault already exists")

        self.vaults[name] = Vault(name,"local",key_path,data_path)

        self.save_vaults()

    def delete_vault(self, name):
        vault = self.vaults[name]

        Path(vault.key_path).unlink(missing_ok=True)
        Path(vault.data_path).unlink(missing_ok=True)

        del self.vaults[name]
        self.save_vaults()