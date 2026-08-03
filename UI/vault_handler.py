from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .UI_handler import UI_handler
from tkinter import messagebox
import tkinter as tk
class Vault_Handler():
    def __init__(self,ui_handler:UI_handler):
          self.ui_handler = ui_handler
    def load_vaults(self, page: int):
            self.selected_vault = ""
            self.ui_handler.render_pages(
                page, self.ui_handler.vault_manager.get_vault_names(), self.ui_handler.frame_handler.subframe_1, self.ui_handler.open_vault, self.new_vault
            )
    def open_vault(self, name: str):
            self.ui_handler.app.selected_vault = name
            self.ui_handler.frame_handler.clear_subframes(self.frame_handler.subframe_2)
    
            vault = self.ui_handler.ui_handler.vaults[name]
            services: list[str] = []
            services = self.ui_handler.vault_manager.get_services(vault)
            if services is None:
                messagebox.showerror("Error","not a valid save type")
    
            self.ui_handler.render_pages(
                0, services, self.frame_handler.subframe_2, self.open_service, self.add_service
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
                
                self.ui_handler.create_vault(vault_name)
                
                new_vault_popup.destroy()
                self.ui_handler.load_vaults(0)
    
            tk.Button(new_vault_popup, text="choose locations", command=add_vault).place(
                relheight=0.1, rely=0.5, relx=0, relwidth=0.3
            )
            new_vault_popup.after(10, self.FONT_MANAGER.apply_fonts, new_vault_popup)
            new_vault_popup.transient(self.root)
            new_vault_popup.grab_set()