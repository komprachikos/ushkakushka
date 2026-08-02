import json
import os
from pathlib import Path
from core.logger import logger

def atomic_json_write(path: Path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def safe_json_load(path: Path, default=None):
    if default is None:
        default = []
    path = Path(path)
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as e:
        # Сохраняем повреждённый файл для анализа
        backup = path.with_suffix(path.suffix + ".corrupted")
        try:
            path.rename(backup)
            logger.error(f"JSON повреждён, сохранён в {backup}: {e}")
        except OSError:
            logger.error(f"JSON повреждён, не удалось создать бэкап: {e}")
        return default