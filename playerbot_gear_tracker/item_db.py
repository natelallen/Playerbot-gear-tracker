import json
from pathlib import Path
import shutil

ITEM_DB_PATH = Path("data/items_db.json")
DEFAULT_JSON = Path("/app/defaults/items_db.json")

DB_PATH = Path("data/database.db")
DEFAULT_DB = Path("/app/defaults/database.db")

ITEM_DB = {}

def load_item_db():
    global ITEM_DB

    ITEM_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not ITEM_DB_PATH.exists():
        shutil.copy(DEFAULT_JSON, ITEM_DB_PATH)

    if not DB_PATH.exists():
        shutil.copy(DEFAULT_DB, DB_PATH)

    with ITEM_DB_PATH.open(encoding="utf-8-sig") as f:
        data = json.load(f)

    if isinstance(data, list):
        normalized = {}
        for item in data:
            item_id = (
                item.get("itemId")
                or item.get("itemID")
                or item.get("itemid")
                or item.get("id")
            )
            if item_id is None:
                continue
            normalized[str(item_id)] = item
        data = normalized

    for item in data.values():
        if "slot" in item and isinstance(item["slot"], str):
            item["slot"] = item["slot"].title()
        if "quality" in item and isinstance(item["quality"], str):
            item["quality"] = item["quality"].lower()

    ITEM_DB = data


def save_item_db():
    with ITEM_DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(ITEM_DB, f, indent=2)
