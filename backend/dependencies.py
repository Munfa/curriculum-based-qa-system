"""Normalization helpers used at the HTTP boundary."""


def normalize_class(value: int | str) -> int | str:
    text = str(value).strip()
    if text.lower().startswith("class "):
        text = text[6:].strip()
    return int(text) if text.isdigit() else text


def normalize_chapter(value: int | str | None) -> int | str | None:
    if value is None:
        return None
    text = str(value).strip()
    if text.lower() == "all chapters":
        return None
    if text.startswith("Chapter-"):
        number = text.split(":", 1)[0].removeprefix("Chapter-")
        if number.isdigit():
            return int(number)
    return int(text) if text.isdigit() else value
