from .UI_handler import UI_handler
import tkinter as tk
class Service_Handler():
    def __init__(self,Ui_Handler:UI_handler) -> None:
        self.UI_Handler = Ui_Handler
    def load_services(self,vault_name):
        self.UI_Handler.render_pages(
            0,
            self.UI_Handler.DATA_HANDLER.services,
            self.UI_Handler.FRAME_HANDLER.subframe_2,
            None,
            self.Add_Service
            )
    def Add_Service(self):
        new_service_popup = tk.Toplevel(
            self.UI_Handler.root,
        )
        self.UI_Handler.scale_toplevel(new_service_popup, 0.5)

        name_entry = tk.Entry(new_service_popup)
        name_entry.place(relheight=0.1, relx=0, rely=0.1, relwidth=1)
        tk.Label(new_service_popup, text="Name").place(
            relheight=0.1, relx=0, rely=0, relwidth=0.5
        )
        
        tk.Button(
            new_service_popup, command=lambda: self.UI_Handler.DATA_HANDLER.add_service(), text="create service"
        ).place(relheight=0.1, rely=0.3, relx=0, relwidth=0.5)

        new_service_popup.after(10, self.FONT_MANAGER.apply_fonts, new_service_popup)
        new_service_popup.transient(self.root)
        new_service_popup.grab_set()