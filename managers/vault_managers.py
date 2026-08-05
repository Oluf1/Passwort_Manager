from pathlib import Path
import json

from UI.vault_handler import get_paths
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from UI.UI_handler import UI_handler
from models.Vault import Vault

class VaultManager:
    def __init__(self,app, vaults_file="vaults.json"):
        self.config_file = vaults_file
        self.vaults = {}
        self.app = app
        self.load_vaults()

    def load_vaults(self):
        with open(self.config_file, "r") as file:
            data = json.load(file)

        for name in data:
            vault_type = data[name]["type"]
            key_path = Path(data[name]["directories"][0])
            data_path = Path(data[name]["directories"][1])

            try:
                self.vaults[name] = Vault(name, vault_type, key_path, data_path)
            except Exception as error:
                self.app.ui_handler.show_error(e)

    def save_vaults(self):
        data = {}
        for vault_name in self.vaults:
            vault = self.vaults[vault_name]
            data[vault_name] = {
                "directories": [str(vault.key_path), str(vault.data_path)],
                "type": vault.vault_type,
            }

        with open(self.config_file, "w") as file:
            json.dump(data, file, indent=2)

    def get_vault_names(self):
        return list(self.vaults.keys())

    def get_vault(self, name)-> Vault:
        vault = self.vaults.get(name)
        if not isinstance(vault,Vault):
            raise ValueError(f"vault: '{vault}' not found")
        return vault

    def create_local_vault(self, name):
        if not name:
            raise Exception("Error: No name chosen")
        if name in self.vaults:
            raise ValueError("Vault already exists")
        
        try:
            paths = get_paths()
        except Exception:
            raise
        key_path = paths[0]
        data_path = paths[1]
        if not data_path or not key_path:
            self.app.ui_handler.show_error("No directory selected")
            return
        self.vaults[name] = Vault(name, "local", key_path, data_path)
        self.save_vaults()

    def delete_vault(self, name):
        vault = self.vaults[name]

        Path(vault.key_path).unlink(missing_ok=True)
        Path(vault.data_path).unlink(missing_ok=True)
        del self.vaults[name]
        self.save_vaults()

        