from models.Theme import Theme

class Themes:
    DARK = Theme(
        background="#1E1E1E",
        button="#2D2D2D",
        text="#FFFFFF",
        top_level="#252526",
    )

    LIGHT = Theme(
        background="#F3F3F3",
        button="#E1E1E1",
        text="#111111",
        top_level="#FFFFFF",
    )

    METRO = Theme(
        background="#202020",
        button="#0078D7",
        text="#FFFFFF",
        top_level="#2B2B2B",
    )
    
    ALL = {
        "dark": DARK,
        "light": LIGHT,
        "metro": METRO,
    }
class ThemeManager:
    def __init__(self) -> None:
        pass
    def change_theme(self,new_theme):
        if new_theme in Themes.ALL.keys():
            self.current_theme = Themes.ALL[new_theme]
        else:
            print("Theme not found")
    @property
    def background(self):
        return self.current_theme.background
    @property
    def button_color(self):
        return self.current_theme.button
    @property 
    def text(self):
        return self.current_theme.text
    @property 
    def top_level_color(self):
        return self.current_theme.top_level
    @property
    def theme_keys(self):
        return Themes.ALL.keys()