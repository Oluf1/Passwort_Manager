import tkinter as tk
def scale_toplevel( window: tk.Toplevel, size: float, theme_manager):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        width = int(screen_width * size)
        height = int(screen_height * size)
        x = int((screen_width - width) * 0.5)
        y = int((screen_height - height) * 0.5)
        window.geometry(f"{width}x{height}+{x}+{y}")
        window.config(bg=theme_manager.top_level_color)
def create_popup(title:str,root:tk.Tk,theme_manager,ui_handler,size:float):
        popup = tk.Toplevel(root)
        popup.title(title)
        popup.resizable(False, False)
        scale_toplevel(popup, size,theme_manager)
        popup.after(10, ui_handler.apply_fonts, popup)
        popup.transient(ui_handler.root)
        popup.grab_set()
        return popup
    