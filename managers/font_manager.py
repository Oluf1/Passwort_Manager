import tkinter.font as tkfont
from tkinter import messagebox
class Font_manager:
    def __init__(self) -> None:
        self.font_family = "Arial"
        self.text_color = ""
        self.widget_color = ""
    def apply_fonts(self,parent):
        for widget in parent.winfo_children():
            if "text" in widget.keys():
                self.fit_font(widget, widget["text"])
    def fit_font(self,widget, text: str):
            try:
                widget.update_idletasks()
                widget_width = widget.winfo_width()
                widget_height = widget.winfo_height()

                max_size = 100
                min_size = 1
                low = min_size
                high = max_size
                best = min_size

                font = tkfont.Font(family=self.font_family, size=1)

                while low <= high:
                    middle = (low + high) // 2
                    font.config(size=middle)
                    text_width = font.measure(text)
                    text_height = font.metrics("linespace")
                    usable_width = widget_width * 0.8

                    if text_width <= usable_width and text_height <= widget_height:
                        best = middle
                        low = middle + 1
                    else:
                        high = middle - 1

                font.configure(size=best)

                if "text" in widget.keys():
                    widget.config(
                        font=font, text=text, fg=self.text_color, bg=self.widget_color
                    )

            except Exception as e:
                messagebox.showerror("Error in fit_font", str(e))