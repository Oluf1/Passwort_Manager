import binascii
import json
import os
from pathlib import Path


class Vault:
    def __init__(self,
                name: str,
                vault_type: str,
                key_path: Path,
                data_path: Path):
        self.data_path = data_path
        self.name = name
        self.key_path = key_path
        self.vault_type = vault_type
        self.set_data_default()
        self.set_key()
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

    def set_data_default(self):
            try:
                if self.data_path.stat().st_size > 0:
                    with open(self.data_path, "r", encoding="utf-8") as file:
                        save = json.load(file)
                else:
                    save = {}
    
            except json.JSONDecodeError:
                save = {}
            save.setdefault("services", {})
            with open(self.data_path, "w", encoding="utf-8") as file:
                json.dump(save, file, indent=2)

    def set_key(self):
            content = self.key_path.read_text().strip()
            try:
                key = binascii.unhexlify(content)
                if len(key) != 32:
                    key = os.urandom(32)
                    self.key_path.write_text(key.hex())
            except binascii.Error:
                raise Exception("Error: not a valid hex string")
