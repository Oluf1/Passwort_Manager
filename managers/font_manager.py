from collections.abc import Callable


class Font_manager:
    def __init__(self,text_color:Callable,widget_color:Callable) -> None:
        self.font_family = "Arial"
        self.text_color = text_color
        self.widget_color = widget_color
    
