from flask import Blueprint, render_template, request, redirect, url_for
from ..db import db
from ..item_db import ITEM_DB

presets_bp = Blueprint("presets", __name__)

# List
@presets_bp.route("/presets")
def presets():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM presets ORDER BY name")
    presets = cur.fetchall()
    conn.close()
    return render_template("presets.html", presets=presets)


# Create
@presets_bp.route("/presets/create", methods=["POST"])
def create_preset():
    name = request.form["name"]

    conn = db()
    conn.execute("INSERT INTO presets (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

    return redirect(url_for("presets.presets"))


# Delete
@presets_bp.route("/presets/<int:preset_id>/delete", methods=["POST"])
def delete_preset(preset_id):
    conn = db()
    conn.execute("DELETE FROM presets WHERE id = ?", (preset_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("presets.presets"))


# Edit
@presets_bp.route("/presets/<int:preset_id>")
def edit_preset(preset_id):
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM presets WHERE id = ?", (preset_id,))
    preset = cur.fetchone()

    if not preset:
        conn.close()
        return "Preset not found", 404

    cur.execute("""
        SELECT id AS pid, item_id, slot, note
        FROM preset_items
        WHERE preset_id = ?
    """, (preset_id,))
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        item = ITEM_DB.get(str(r["item_id"]))
        if not item:
            continue
        items.append({
            "pid": r["pid"],
            "item_id": r["item_id"],
            "slot": r["slot"],
            "preset_note": r["note"],
            "name": item.get("name"),
            "quality": item.get("quality"),
            "dungeon": item.get("dungeon"),
            "boss": item.get("boss"),
        })

    return render_template("edit_preset.html",
                           preset=preset,
                           items=items)


# Add item
@presets_bp.route("/presets/<int:preset_id>/add_item", methods=["POST"])
def add_preset_item(preset_id):
    item_id = request.form["item_id"]

    item = ITEM_DB.get(str(item_id))
    slot = item.get("slot")

    conn = db()
    conn.execute("""
        INSERT INTO preset_items (preset_id, item_id, slot, note)
        VALUES (?, ?, ?, NULL)
    """, (preset_id, item_id, slot))
    conn.commit()
    conn.close()

    return redirect(url_for("presets.edit_preset", preset_id=preset_id))


# Delete preset item
@presets_bp.route("/presets/items/<int:pid>/delete", methods=["POST"])
def delete_preset_item(pid):
    conn = db()
    cur = conn.cursor()

    cur.execute("SELECT preset_id FROM preset_items WHERE id = ?", (pid,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return redirect(url_for("presets.presets"))

    preset_id = row["preset_id"]

    conn.execute("DELETE FROM preset_items WHERE id = ?", (pid,))
    conn.commit()
    conn.close()

    return redirect(url_for("presets.edit_preset", preset_id=preset_id))

# Apply preset
@presets_bp.route("/characters/<int:char_id>/apply_preset", methods=["POST"])
def apply_preset(char_id):
    preset_id = request.form["preset_id"]

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT item_id, slot, note
        FROM preset_items
        WHERE preset_id = ?
    """, (preset_id,))
    preset_items = cur.fetchall()

    for row in preset_items:
        item_id = row["item_id"]
        slot = row["slot"]
        preset_note = row["note"]

        cur.execute("""
            INSERT INTO wishlist (character_id, item_id, slot, acquired, note)
            VALUES (?, ?, ?, 0, ?)
        """, (char_id, item_id, slot, preset_note))

    conn.commit()
    conn.close()

    return redirect(url_for("characters.character_detail", char_id=char_id))

# Edit preset
@presets_bp.route("/presets/items/<int:preset_item_id>/note", methods=["POST"])
def update_preset_note(preset_item_id):
    note = request.form.get("note", "").strip()
    preset_id = request.form.get("preset_id")

    conn = db()
    conn.execute("""
        UPDATE preset_items
        SET note = ?
        WHERE id = ?
    """, (note, preset_item_id))
    conn.commit()
    conn.close()

    return redirect(url_for("presets.edit_preset", preset_id=preset_id))
