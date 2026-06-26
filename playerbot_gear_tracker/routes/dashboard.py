from flask import Blueprint, render_template
from playerbot_gear_tracker.db import db
from playerbot_gear_tracker.item_db import ITEM_DB

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard():
    conn = db()
    cur = conn.cursor()

    # Load all wishlist entries that are NOT acquired
    cur.execute("""
        SELECT wishlist.character_id,
               wishlist.item_id,
               wishlist.acquired,
               characters.name AS char_name,
               characters.class AS class,
               accounts.name AS account_name
        FROM wishlist
        JOIN characters ON characters.id = wishlist.character_id
        JOIN accounts ON accounts.id = characters.account_id
        WHERE wishlist.acquired = 0
    """)
    rows = cur.fetchall()
    conn.close()

    dungeon_map = {}

    for row in rows:
        item = ITEM_DB.get(str(row["item_id"]))
        if not item:
            continue

        dungeon = item.get("dungeon") or "Unknown"
        boss = item.get("boss") or "Unknown"

        if dungeon not in dungeon_map:
            dungeon_map[dungeon] = {
                "dungeon": dungeon,
                "needed": 0,
                "chars": {}
            }

        dungeon_map[dungeon]["needed"] += 1

        char_key = row["char_name"]

        if char_key not in dungeon_map[dungeon]["chars"]:
            dungeon_map[dungeon]["chars"][char_key] = {
                "char_name": row["char_name"],
                "account_name": row["account_name"],
                "class": row["class"],
                "loot": []
            }

        dungeon_map[dungeon]["chars"][char_key]["loot"].append({
            "item_name": item.get("name"),
            "boss_name": boss,
            "quality": item.get("quality")
        })

    # Convert dict → list and sort by needed desc
    dungeon_data = list(dungeon_map.values())
    dungeon_data.sort(key=lambda d: d["needed"], reverse=True)

    return render_template("dashboard.html", dungeons=dungeon_data)
