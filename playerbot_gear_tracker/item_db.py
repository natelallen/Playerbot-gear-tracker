import json
from pathlib import Path

ITEM_DB_PATH = Path("data/items_db.json")
ITEM_DB = {}

def load_item_db():
    global ITEM_DB

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
