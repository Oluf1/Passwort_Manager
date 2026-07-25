import tkinter as tk
#from tkinter import messagebox, simpledialog
from typing import Callable
from main_menu import load_main_menu
from managers import Font_manager
from main import App#temporary so as to not break parts 
from .main_menu import load_main_menu
class UI_handler:
    def __init__(self,
                 Font_Manager:Font_manager,
                 App:App) -> None:
        self.root = tk.Tk()
        
        self.Font_Manager = Font_Manager
        self.App = App
        self.apply_fonts = self.Font_Manager.apply_fonts
        
    def load_vaults(self,page:int):
        self.App.load_vaults(0)
    def load_config(self):
        self.App.Load_config()
    def load_main_menu(self):
        load_main_menu(self)
    
    
    def setup(self):
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)
            
        self.root.title("Password Manager")
        self.background = "F3F3F3" #Default bg color to avoid Errors
        
        self.create_frames()
        
        
        load_main_menu(self)
    
      
    def create_frames(self): 
        border_width = 2

        self.main_frame =   tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.main_frame.place(relheight=1, relwidth=0.2, relx=0, rely=0)
        self.subframe_1 = tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_1.place(relheight=1, relwidth=0.15, relx=0.2, rely=0)
        self.subframe_2 = tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_2.place(relheight=1, relwidth=0.25, relx=0.35, rely=0)
        self.subframe_3 = tk.Frame(self.root, borderwidth=border_width, relief="solid")
        self.subframe_3.place(relheight=1, relwidth=0.4, relx=0.6)

        self.subframe_list = [self.subframe_1, self.subframe_2, self.subframe_3]
    def apply_theme_on_frames(self):
        for frame in self.subframe_list:
            frame.configure(bg=self.background)
        self.main_frame.config(bg=self.background)
        