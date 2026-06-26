from flask import Blueprint, request, redirect, url_for
from ..db import db
from ..item_db import ITEM_DB

wishlist_bp = Blueprint("wishlist", __name__)

@wishlist_bp.route("/characters/<int:char_id>/wishlist/add", methods=["POST"])
def add_wishlist_item(char_id):
    item_id = request.form["item_id"]

    item = ITEM_DB.get(str(item_id))
    if not item:
        return redirect(url_for("characters.character_detail", char_id=char_id))

    slot = item.get("slot")

    if item_id and slot:
        conn = db()
        conn.execute("""
            INSERT INTO wishlist (character_id, slot, item_id, acquired)
            VALUES (?, ?, ?, 0)
        """, (char_id, slot, item_id))
        conn.commit()
        conn.close()

    return redirect(url_for("characters.character_detail", char_id=char_id))


@wishlist_bp.route("/wishlist/<int:w_id>/toggle", methods=["POST"])
def toggle_wishlist(w_id):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT acquired, character_id FROM wishlist WHERE id = ?", (w_id,))
    row = cur.fetchone()
    if row:
        new_val = 0 if row["acquired"] else 1
        conn.execute("UPDATE wishlist SET acquired = ? WHERE id = ?", (new_val, w_id))
        conn.commit()
        char_id = row["character_id"]
        conn.close()
        return redirect(url_for("characters.character_detail", char_id=char_id))
    conn.close()
    return redirect(url_for("dashboard.dashboard"))


@wishlist_bp.route("/wishlist/<int:w_id>/delete", methods=["POST"])
def delete_wishlist_item(w_id):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT character_id FROM wishlist WHERE id = ?", (w_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return redirect(url_for("dashboard.dashboard"))

    char_id = row["character_id"]
    conn.execute("DELETE FROM wishlist WHERE id = ?", (w_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("characters.character_detail", char_id=char_id))
