import tkinter as tk
from .main_menu import load_main_menu
from managers import Font_manager, ThemeManager,ConfigManager,VaultManager
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import App #avoids Circular Importing#temporary so as to not break parts 
from .frame_handler import Frame_Handler
from .page_handler import render_pages
from .config_ui import load_config 
from .font_handler import apply_fonts
from .toplevel_handler import scale_toplevel,create_popup
from .vault_handler import Vault_Handler
class UI_handler:
    def __init__(self,
                 Font_Manager:Font_manager,
                 theme_manager:ThemeManager,
                 config:ConfigManager,
                 vault_manager:VaultManager,
                 App:"App") -> None:
        
        self.vault_manager = vault_manager
        self.theme_manager = theme_manager
        self.font_manager = Font_Manager
        self.config = config
        self.app = App
        self.apply_fonts = self.font_manager.apply_fonts
        self.vault_handler = Vault_Handler(self)
        
        
        self.setup()
        
    def setup(self):
        # Setting up base properties of Root
        self.root = tk.Tk()
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)
            
        self.root.title("Password Manager")

        self.frame_handler = Frame_Handler(self)
        
        load_main_menu(self)    
        
    def load_vaults(self,page:int):
        self.vault_handler.load_vaults(page)

    def open_vault(self,name:str):
        self.vault_handler.open_vault(name)

    def load_config(self):
        load_config(self) 
        
    def load_main_menu(self):
        load_main_menu(self)

    def apply_fonts(self,parent):
        apply_fonts(parent,self.font_manager)
    
    def render_pages(self,page,items,frame,open_function,add_command,filter_str=None):
        render_pages(self,page,items,frame,open_function,add_command,filter_str)
    
    def apply_fonts(self,parent:tk.Frame):
        self.font_handler.apply_fonts(parent)

    def scale_toplevel(self,window: tk.Toplevel, size: float):
        scale_toplevel(window,size,self.theme_manager)

    def create_popup(self,title):
        create_popup(title,self.root,self.theme_manager)