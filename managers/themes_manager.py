from dataclasses import dataclass
@dataclass(frozen=True)
class Theme:
    background: str
    button: str
    text: str
    top_level: str

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