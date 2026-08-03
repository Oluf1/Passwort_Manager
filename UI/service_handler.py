import tkinter as tk
import json
from tkinter import messagebox
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .UI_handler import UI_handler

class ServiceHandler():
    def __init__(self,ui_handler:"UI_handler"):
        self.ui_handler = ui_handler
    def add_service(self): #KEEP UI
            new_service_popup =self.ui_handler.create_popup("add service")

            name_entry = tk.Entry(new_service_popup)
            name_entry.place(relheight=0.1, relx=0, rely=0.1, relwidth=1)
            tk.Label(new_service_popup, text="Name").place(
                relheight=0.1, relx=0, rely=0, relwidth=0.5
            )

            def create_service():# move (password_data_manager)
                new_name = name_entry.get()

                services: list[str] = []
                vault = self.ui_handler.vault_manager.vaults[self.selected_vault]
                try:
                    vault.add_service(new_name)
                except Exception as e:
                    messagebox.showerror("Error",e)
                new_service_popup.destroy()
                
                self.ui_handler.open_vault(self.selected_vault)

            tk.Button(
                new_service_popup, command=create_service, text="create service"
            ).place(relheight=0.1, rely=0.3, relx=0, relwidth=0.5)

            new_service_popup.after(10, self.FONT_MANAGER.apply_fonts, new_service_popup)
            new_service_popup.transient(self.root)
            new_service_popup.grab_set()

    def open_service(self, name: str):# KEEP
        self.selected_service = name

        self.frame_handler.clear_subframes(self.frame_handler.subframe_3)

        vault = self.VAULTMANAGER.vaults[self.selected_vault]
        Mails: list = []
        if vault.vault_type == "local":
            location = vault.data_path
            with open(location) as f:
                data = json.load(f)

            for ele in data["services"][name]:
                Mails.append((ele["Mail"], ele["count"]))
            self.ui_handler.render_pages(0, Mails, self.frame_handler.subframe_3, self.open_mail, self.add_mail)
