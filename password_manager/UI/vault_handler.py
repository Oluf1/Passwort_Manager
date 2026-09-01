from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .UI_handler import UI_handler
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

# dependencies from ui_handler: render_pages, selected_vault, clear_subframes, vaultmanager(vaults+get_vault_names+create_local_vault+load_vaults), create_popup

class Vault_Handler():
    def __init__(self,ui_handler:"UI_handler"):
          self.ui_handler = ui_handler
          
    def load_vaults(self, page: int):
            self.selected_vault = ""
            self.ui_handler.render_pages(
                page, self.ui_handler.vault_manager.get_vault_names(), self.ui_handler.frame_handler.subframe_1, self.ui_handler.open_vault, self.ui_handler.new_vault
            )
    def open_vault(self, name: str):
            self.ui_handler.app.selected_vault = name
            self.ui_handler.frame_handler.clear_subframes(self.ui_handler.frame_handler.subframe_2)
    
            vault = self.ui_handler.vault_manager.vaults[name]
            services: list[str] = []
            try:
                services = vault.get_services()
            except Exception as E:
                self.ui_handler.messagebox_error(f"{E}")
                return
    
            self.ui_handler.render_pages(
                0, services, self.ui_handler.frame_handler.subframe_2, self.ui_handler.open_service, self.ui_handler.add_service
            )



    def new_vault(self): 
            new_vault_popup = self.ui_handler.create_popup("add vault")
    
            tk.Label(new_vault_popup, text="New vault Name").place(
                relheight=0.1, relx=0, rely=0, relwidth=0.4
            )
            vault_name_entry = tk.Entry(new_vault_popup)
    
            vault_name_entry.place(relheight=0.15, relwidth=1, relx=0, rely=0.1)
    
            vault_type = tk.StringVar(value="local")
    
            tk.Label(new_vault_popup, text="vault type").place(
                relheight=0.1, relx=0, rely=0.27, relwidth=0.4
            )
            tk.Radiobutton(
                new_vault_popup, text="Local", value="local", variable=vault_type
            ).place(relheight=0.1, relx=0, rely=0.4, relwidth=0.4)
            tk.Radiobutton(
                new_vault_popup, text="server", value="server", variable=vault_type
            ).place(relheight=0.1, relx=0.5, rely=0.4, relwidth=0.4)
    
            def add_vault(): # move (vault_manager) partially done
                if vault_type.get() == "server":
                    messagebox.showerror("Error", "Server saving not yet implemented")
                    return
                vault_name = vault_name_entry.get()
                try:
                    self.ui_handler.vault_manager.create_local_vault(vault_name)
                except Exception as e:
                     messagebox.showerror("Error",f"{e}")
                new_vault_popup.destroy()

                self.ui_handler.load_vaults(0)
    
            tk.Button(new_vault_popup, text="choose locations", command=add_vault).place(
                relheight=0.1, rely=0.5, relx=0, relwidth=0.3
            )
            



def get_paths():
        data_dir = filedialog.askopenfilename(
            initialdir="/",
            title="select save directory",
            filetypes=(("json files", "*.json*"),),
        )
        if not data_dir:
            raise Exception("Error: No data directory chosen")
        key_dir = filedialog.askopenfilename(
            initialdir="/",
            title="select key directory",
            filetypes=(("Text files", "*.txt*"),),
        )
        if not key_dir:
            raise Exception("Error: No key directory chosen")
        
        data_path = Path(data_dir)
        key_path = Path(key_dir)
        return data_path, key_path