from .config_manager import ConfigManager
from .font_manager import Font_manager
from .themes_manager import ThemeManager
from.vault_managers import VaultManager

CONFIG = ConfigManager()
THEME_MANAGER = ThemeManager()

CONFIG.load()
THEME_MANAGER.change_theme(CONFIG.theme_name)
FONT_MANAGER = Font_manager(
    THEME_MANAGER.button_color,
    THEME_MANAGER.text
    )

FONT_MANAGER.font_family = CONFIG.font_family