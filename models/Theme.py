from dataclasses import dataclass
@dataclass(frozen=True)
class Theme:
    background: str
    button: str
    text: str
    top_level: str