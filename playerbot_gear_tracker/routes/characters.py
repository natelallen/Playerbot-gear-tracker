from flask import Blueprint, render_template, request, redirect, url_for
from ..db import db
from ..item_db import ITEM_DB

characters_bp = Blueprint("characters", __name__)

@characters_bp.route("/characters")
def characters():
    conn = db()
    cur = conn.cursor()
    cur.execute("""
        SELECT characters.*, accounts.name AS account_name
        FROM characters
        JOIN accounts ON accounts.id = characters.account_id
        ORDER BY accounts.name, characters.name
    """)
    chars = cur.fetchall()

    cur.execute("SELECT * FROM accounts ORDER BY name")
    accounts = cur.fetchall()
    conn.close()
    return render_template("characters.html", characters=chars, accounts=accounts)


@characters_bp.route("/characters/add", methods=["GET", "POST"])
def add_character():
    conn = db()
    cur = conn.cursor()

    if request.method == "POST":
        account_id = request.form["account_id"]
        name = request.form["name"]
        char_class = request.form["class"]
        spec = request.form["spec"]

        conn.execute("""
            INSERT INTO characters (account_id, name, class, spec)
            VALUES (?, ?, ?, ?)
        """, (account_id, name, char_class, spec))

        conn.commit()
        conn.close()
        return redirect(url_for("characters.characters"))

    cur.execute("SELECT * FROM accounts ORDER BY name")
    accounts = cur.fetchall()
    conn.close()

    return render_template("add_character.html", accounts=accounts)


@characters_bp.route("/characters/<int:char_id>/delete", methods=["POST"])
def delete_character(char_id):
    conn = db()
    conn.execute("DELETE FROM characters WHERE id = ?", (char_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("characters.characters"))


@characters_bp.route("/characters/<int:char_id>")
def character_detail(char_id):
    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT characters.*, accounts.name AS account_name
        FROM characters
        JOIN accounts ON accounts.id = characters.account_id
        WHERE characters.id = ?
    """, (char_id,))
    char = cur.fetchone()

    cur.execute("""
        SELECT id, slot, acquired, item_id
        FROM wishlist
        WHERE character_id = ?
    """, (char_id,))
    rows = cur.fetchall()

    cur.execute("SELECT * FROM presets ORDER BY name")
    presets = cur.fetchall()

    conn.close()

    wishlist = []
    for w in rows:
        item = ITEM_DB.get(str(w["item_id"]), {})
        wishlist.append({
            "id": w["id"],
            "slot": w["slot"],
            "acquired": w["acquired"],
            "name": item.get("name"),
            "dungeon": item.get("dungeon"),
            "boss": item.get("boss"),
            "quality": item.get("quality"),
        })

    return render_template(
        "character_detail.html",
        char=char,
        wishlist=wishlist,
        presets=presets
    )
