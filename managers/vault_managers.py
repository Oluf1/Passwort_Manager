from pathlib import Path
import json
import binascii
import os
from tkinter import filedialog, messagebox
from dataclasses import dataclass


@dataclass
class Vault:
    name: str
    vault_type: str
    key_path: Path
    data_path: Path
    def get_services(self) -> list[str]:
        if self.vault_type == "local":
            location = self.data_path

            with open(location) as f:
                data = json.load(f)
                services = list(data["services"].keys())
                return services
    def add_service(self,new_name:str)-> None:
        with open(self.data_path)as services:
            data = json.load(services)
        if new_name in list(data["services"].keys()):
            raise Exception("service already exists")
        data["services"][new_name] = []
        with open(self.data_path, "w") as file:
            json.dump(data, file, indent=2)

class VaultManager:
    def __init__(self, vaults_file="vaults.json"):
        self.config_file = vaults_file
        self.vaults = {}
        self.load_vaults()

    def load_vaults(self):
        with open(self.config_file, "r") as file:
            data = json.load(file)

        for name in data:
            vault_type = data[name]["type"]
            key_path = data[name]["directories"][0]
            data_path = data[name]["directories"][1]

            self.vaults[name] = Vault(name, vault_type, key_path, data_path)

    def save_vaults(self):
        data = {}
        for vault_name in self.vaults:
            vault = self.vaults[vault_name]
            data[vault_name] = {
                "directories": [vault.key_path, vault.data_path],
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

    def create_vault(self, name):
        if name in self.vaults:
            raise ValueError("Vault already exists")

        paths = self.get_paths()
        key_path = paths[0]
        data_path = paths[1]
        if not data_path or not key_path:
            messagebox.showerror("Error", "No directory selected")
            return
        self.vaults[name] = Vault(name, "local", key_path, data_path)
        self.set_data_default(data_path)
        self.set_key(key_path)

        self.save_vaults()

    def set_key(self, key_path):
        content = key_path.read_text().strip()
        try:
            key = binascii.unhexlify(content)
            if len(key) != 32:
                key = os.urandom(32)
                key_path.write_text(key.hex())
        except binascii.Error:
            messagebox.showerror("Error", "not a valid hex string")

    def set_data_default(self, data_path):
        try:
            if data_path.stat().st_size > 0:
                with open(data_path, "r", encoding="utf-8") as file:
                    save = json.load(file)
            else:
                save = {}

        except json.JSONDecodeError:
            save = {}
        save.setdefault("services", {})
        with open(data_path, "w", encoding="utf-8") as file:
            json.dump(save, file, indent=2)

    def get_paths(self):
        data_dir = filedialog.askopenfilename(
            initialdir="/",
            title="select save directory",
            filetypes=(("json files", "*.json*"),),
        )
        key_dir = filedialog.askopenfilename(
            initialdir="/",
            title="select key directory",
            filetypes=(("Text files", "*.txt*"),),
        )

        data_path = Path(data_dir)
        key_path = Path(key_dir)
        return data_path, key_path

    def delete_vault(self, name):
        vault = self.vaults[name]

        Path(vault.key_path).unlink(missing_ok=True)
        Path(vault.data_path).unlink(missing_ok=True)
        del self.vaults[name]
        self.save_vaults()

        