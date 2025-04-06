from dataclasses import dataclass
from enum import Enum

from pydantic_settings import BaseSettings


class Theme(str, Enum):
    DEFAULT = "default"
    FRIENDLY = "friendly"
    COLORFUL = "colorful"
    EMACS = "emacs"


class Language(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "cpp"
    HTML = "html"
    CSS = "css"


@dataclass
class ImageConfig:
    width: int = 800
    height: int = 600
    padding: int = 20
    background_color: str = "#ffffff"
    watermark: bool = False


class Settings(BaseSettings):
    ALLOWED_FILE_TYPES: list = [".txt", ".py", ".js", ".java", ".cpp", ".html", ".css"]
    MAX_FILE_SIZE_MB: int = 5
    MAX_CODE_LENGTH: int = 5000
    DEFAULT_THEME: Theme = Theme.DEFAULT
    DEFAULT_LANGUAGE: Language = Language.PYTHON

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
