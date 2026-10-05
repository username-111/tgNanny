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


def _parse_allowed_user_ids(raw_value: str) -> set[int]:
    values = [item.strip() for item in raw_value.split(",")]
    values = [item for item in values if item]
    if not values:
        raise RuntimeError("Параметр 'allowed_user_ids' в config.ini не должен быть пустым.")

    parsed_ids: set[int] = set()
    for value in values:
        try:
            parsed_ids.add(int(value))
        except ValueError as exc:
            raise RuntimeError(
                "Параметр 'allowed_user_ids' в config.ini должен содержать "
                "только целые числа, разделённые запятыми."
            ) from exc

    return parsed_ids


_telegram = _load_config()
BOT_TOKEN = _get_required_value(_telegram, "bot_token")
ALLOWED_USER_IDS = _parse_allowed_user_ids(_get_required_value(_telegram, "allowed_user_ids"))
