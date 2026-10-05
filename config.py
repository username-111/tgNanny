import configparser
from pathlib import Path


CONFIG_PATH = Path(__file__).with_name("config.ini")


def _load_config() -> configparser.SectionProxy:
    if not CONFIG_PATH.exists():
        raise RuntimeError(
            "Файл config.ini не найден. "
            "Скопируйте config.example.ini в config.ini и заполните реальные значения."
        )

    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")

    if "telegram" not in parser:
        raise RuntimeError("В config.ini отсутствует секция [telegram].")

    return parser["telegram"]


def _get_required_value(section: configparser.SectionProxy, key: str) -> str:
    value = section.get(key, "").strip()
    if not value:
        raise RuntimeError(f"В config.ini не задан параметр '{key}' в секции [telegram].")
    return value


_telegram = _load_config()
BOT_TOKEN = _get_required_value(_telegram, "bot_token")

try:
    ALLOWED_USER_ID = int(_get_required_value(_telegram, "allowed_user_id"))
except ValueError as exc:
    raise RuntimeError("Параметр 'allowed_user_id' в config.ini должен быть целым числом.") from exc
