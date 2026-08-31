import tkinter as tk
from typing import TYPE_CHECKING, Callable

from .main_menu import load_main_menu

if TYPE_CHECKING:
    from main import App  #avoids Circular Importing#temporary so as to not break parts 
    from managers import ConfigManager, Font_manager, ThemeManager, VaultManager
from tkinter import messagebox

from .config_ui import ConfigUI
from .font_handler import apply_fonts
from .frame_handler import Frame_Handler
from .mail_handler import MailManager
from .page_handler import render_pages
from .service_handler import ServiceHandler
from .toplevel_handler import create_popup, scale_toplevel
from .vault_handler import Vault_Handler
from dataclasses import dataclass


@dataclass 
class UiConfigDependencies: ## Do This for most if not all dependencies
    _get_items_per_page: Callable[[], int]
    _supported_kdfs: Callable
    @property
    def items_per_page(self):
        self._get_items_per_page()

class UI_handler:
    def __init__(self,
                 Font_Manager:"Font_manager",
                 theme_manager:"ThemeManager",
                 config:"ConfigManager",
                 vault_manager:"VaultManager",
                 App:"App") -> None:
        
        self.vault_manager = vault_manager
        self.theme_manager = theme_manager
        self.font_manager = Font_Manager
        self.config = config
        self.app = App
        
        
        
        self.setup()
        
    def setup(self):
        # Setting up base properties of Root
        self.root = tk.Tk()
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)
            
        self.root.title("Password Manager")
        self.config_ui = ConfigUI(self)
        self.frame_handler = Frame_Handler(self)
        self.vault_handler = Vault_Handler(self)
        self.service_handler = ServiceHandler(self)
        self.mail_manager= MailManager(self)
        
        load_main_menu(self)    
        
    def load_vaults(self,page:int):
        self.vault_handler.load_vaults(page)

    def open_vault(self,name:str):
        self.vault_handler.open_vault(name)

    def load_config(self):
        self.config_ui.load_config()

    def new_vault(self):
        self.vault_handler.new_vault()
        
    def load_main_menu(self):
        load_main_menu(self)

    def apply_fonts(self,parent:tk.Frame):
        apply_fonts(parent,self)
    
    def render_pages(self,page,items:list[str],frame,open_function,add_command,filter_str=None):
        render_pages(self,page,items,frame,open_function,add_command,filter_str)

    def scale_toplevel(self,window: tk.Toplevel, size: float):
        scale_toplevel(window,size,self.theme_manager)

    def create_popup(self,title,size=0.5):
        return create_popup(title,self.root,self.theme_manager,self,size)

    def open_service(self,name:str):
        self.service_handler.open_service(name)
    def add_service(self):
        self.service_handler.add_service()

    def open_mail(self,name:str):
        self.mail_manager.open_mail(name)
    def add_mail(self):
        self.mail_manager.add_mail()

    def messagebox_error(self,error:str)->None:
        messagebox.showerror("Error",error)