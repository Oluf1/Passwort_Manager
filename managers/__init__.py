from .config_manager import ConfigManager
from .themes_manager import ThemeManager
from .vault_managers import VaultManager
from .font_manager import Font_manager

CONFIG = ConfigManager()
THEME_MANAGER = ThemeManager()
VAULT_MANAGER = VaultManager()
FONT_MANAGER = Font_manager()

CONFIG.load()
THEME_MANAGER.change_theme(CONFIG.theme_name)
FONT_MANAGER.widget_color = THEME_MANAGER.button_color
FONT_MANAGER.text_color = THEME_MANAGER.text
FONT_MANAGER.font_family = CONFIG.font_family