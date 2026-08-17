from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from.UI_handler import UI_handler
import tkinter as tk
class Frame_Handler:
    def __init__(self,ui_handler:"UI_handler") -> None:
        self.ui_handler = ui_handler
        self.create_frames()
    def create_frames(self): 
        border_width = 2

        self.main_frame =   tk.Frame(self.ui_handler.root, borderwidth=border_width, relief="solid")
        self.main_frame.place(relheight=1, relwidth=0.2, relx=0, rely=0)
        self.subframe_1 = tk.Frame(self.ui_handler.root, borderwidth=border_width, relief="solid")
        self.subframe_1.place(relheight=1, relwidth=0.15, relx=0.2, rely=0)
        self.subframe_2 = tk.Frame(self.ui_handler.root, borderwidth=border_width, relief="solid")
        self.subframe_2.place(relheight=1, relwidth=0.25, relx=0.35, rely=0)
        self.subframe_3 = tk.Frame(self.ui_handler.root, borderwidth=border_width, relief="solid")
        self.subframe_3.place(relheight=1, relwidth=0.4, relx=0.6)

        self.subframe_list = [self.subframe_1, self.subframe_2, self.subframe_3]
        self.apply_theme_on_frames()
    
    def apply_theme_on_frames(self):
        for frame in self.subframe_list:
            frame.configure(bg=self.ui_handler.theme_manager.background)
        self.main_frame.config(bg=self.ui_handler.theme_manager.background)
    
    def clear_subframes(self, subframe: tk.Frame): #move (UI handler)
        index = self.subframe_list.index(subframe)
        for frame in self.subframe_list[index:]:
            for widget in frame.winfo_children():
                widget.destroy()