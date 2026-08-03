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
