from flask import Blueprint, render_template
from playerbot_gear_tracker.db import db
from playerbot_gear_tracker.item_db import ITEM_DB

dungeons_bp = Blueprint("dungeons", __name__)

@dungeons_bp.route("/dungeons/<dungeon>")
def dungeon_detail(dungeon):
    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT wishlist.character_id,
               wishlist.item_id,
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

    filtered = []

    for row in rows:
        item = ITEM_DB.get(str(row["item_id"]))
        if not item:
            continue

        if item.get("dungeon") == dungeon:
            filtered.append({
                "char_name": row["char_name"],
                "account_name": row["account_name"],
                "class": row["class"],
                "slot": item.get("slot"),
                "item_name": item.get("name"),
                "boss": item.get("boss"),
                "quality": item.get("quality")
            })

    return render_template("dungeon_detail.html",
                           dungeon=dungeon,
                           rows=filtered)
