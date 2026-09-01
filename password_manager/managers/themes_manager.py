import json

from models.Theme import Theme


class Themes:
    def __init__(self):
        with open("themes.json", "r") as themes_file:
            data = json.load(themes_file)

        self.all = {
            name: Theme(**values)
            for name, values in data.items()
        }

class ThemeManager:
    def __init__(self) -> None:
        self.theme = Themes()
    def change_theme(self,new_theme):
        if new_theme in self.theme.all:
            self.current_theme = self.theme.all[new_theme]
        else:
            print("Theme not found")
    @property
    def background(self):
        return self.current_theme.background
    
    def button_color(self):
        return self.current_theme.button
    
    def text(self):
        return self.current_theme.text
    @property 
    def top_level_color(self):
        return self.current_theme.top_level
    @property
    def theme_keys(self):
        return self.theme.all.keys()