import managers as managers
from UI.UI_handler import UI_handler


class App:
    CONFIG = managers.CONFIG
    THEME_MANAGER = managers.THEME_MANAGER
    FONT_MANAGER = managers.FONT_MANAGER
    
    def __init__(self):
        self.VAULTMANAGER = managers.VaultManager(self)
        self.ui_handler = UI_handler(
            self.FONT_MANAGER,
            self.THEME_MANAGER,
            self.CONFIG,
            self.VAULTMANAGER,
            self
            )
        

        
        self.frame_handler = self.ui_handler.frame_handler
        
        self.setup()


        

    def setup(self):
        
        
        self.VAULTMANAGER.load_vaults() 
        self.selected_vault = ""
        self.selected_service = ""
        self.supported_kdfs = ["Argon2", "PBKDF2"]
        self.THEME_MANAGER.change_theme(self.CONFIG.theme_name)
        
        
        self.ui_handler.load_main_menu()
        self.ui_handler.root.mainloop()

    

if __name__ == "__main__":
    App()
