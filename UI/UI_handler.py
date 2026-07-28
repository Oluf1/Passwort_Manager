import tkinter as tk
from .main_menu import load_main_menu
from managers import Font_manager, ThemeManager,ConfigManager,VaultManager
from main import App#temporary so as to not break parts 
from .frame_handler import Frame_Handler
from .page_handler import render_pages
from .load_config import load_config 
class UI_handler:
    def __init__(self,
                 Font_Manager:Font_manager,
                 theme_manager:ThemeManager,
                 config:ConfigManager,
                 vault_manager:VaultManager,
                 App:App) -> None:
        
        self.vault_manager = vault_manager
        self.theme_manager = theme_manager
        self.font_manager = Font_Manager
        self.config = config
        self.app = App
        self.apply_fonts = self.font_manager.apply_fonts
        
        self.frame_handler = Frame_Handler(self)
        
    def setup(self):
        # Setting up base properties of Root
        self.root = tk.Tk()
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)
            
        self.root.title("Password Manager")

        load_main_menu(self)    
    def load_vaults(self,page:int):
        self.app.load_vaults(0)
        
    def load_config(self):
        load_config(self) #temporarily using app. since it hasn't been added to UI_handler yet
        
    def load_main_menu(self):
        load_main_menu(self)
    
    def render_pages(self,page,items,frame,open_function,add_command,filter_str=None):
        render_pages(self,page,items,frame,open_function,add_command,filter_str)
    
    
   
    
      
        