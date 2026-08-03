from .UI_handler import UI_handler
from tkinter import messagebox
class Vault_Handler():
    def __init__(self,ui_handler:UI_handler):
          self.ui_handler = ui_handler
    def load_vaults(self, page: int):#move (UI handler)
            self.selected_vault = ""
            self.ui_handler.render_pages(
                page, self.ui_handler.vault_manager.get_vault_names(), self.ui_handler.frame_handler.subframe_1, self.ui_handler.open_vault, self.ui_handler.new_vault
            )
    def open_vault(self, name: str): #move (UI handler)
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