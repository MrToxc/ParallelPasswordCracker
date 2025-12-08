import os

def get_file_characters(path):
    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    chars = set()
    for ch in content:
        chars.add(ch)

    return chars
