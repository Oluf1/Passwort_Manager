import tkinter as tk
from .UI_handler import UI_handler
def load_main_menu(UI_Handler:UI_handler):#move (UI handler)
        

        name_label = tk.Label(UI_Handler.frame_handler.main_frame, text="Password Manager")
        open_vaults_button = tk.Button(
            UI_Handler.frame_handler.main_frame,
            text="Vaults",
            bg="royalblue",
            command=lambda: UI_Handler.load_vaults(0),
        )
        name_label.place(relx=0, rely=0, relwidth=0.95, relheight=0.1)
        config_button = tk.Button(
            UI_Handler.frame_handler.main_frame, text="config", bg="lightgrey", command=UI_Handler.load_config
        )
        open_vaults_button.place(
            relx=0,
            rely=0.1,
            relwidth=1,
            relheight=0.1,
        )
        config_button.place(relx=0, rely=0.21, relwidth=1, relheight=0.1)
        UI_Handler.root.after(10, lambda: UI_Handler.font_manager.apply_fonts(UI_Handler.frame_handler.main_frame))