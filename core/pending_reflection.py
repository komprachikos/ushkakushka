import json
from pathlib import Path


FILE = Path("memory/pending_reflection.json")


def save_pending_reflection(data):

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def load_pending_reflection():

    if not FILE.exists():
        return None

    with open(
        FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def clear_pending_reflection():

    if FILE.exists():
        FILE.unlink()