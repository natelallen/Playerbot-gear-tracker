from flask import Blueprint, render_template, request, jsonify
from ..item_db import ITEM_DB, save_item_db

items_bp = Blueprint("items", __name__)

@items_bp.route("/edit-items")
def edit_items():
    return render_template("edit_items.html")


@items_bp.route("/items/search")
def search_items():
    q = request.args.get("q", "").lower()
    results = []

    for item_id, item in ITEM_DB.items():
        name = item.get("name", "")
        if q in name.lower():
            results.append({
                "id": item_id,
                "name": name,
                "slot": item.get("slot", ""),
                "quality": item.get("quality", "")
            })
        if len(results) >= 25:
            break

    return jsonify(results)


@items_bp.route("/items/<item_id>")
def get_item(item_id):
    item = ITEM_DB.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"id": item_id, **item})


@items_bp.route("/items/add", methods=["POST"])
def add_item():
    data = request.json

    required = ["id", "name", "slot", "quality"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    item_id = str(data["id"])
    if item_id in ITEM_DB:
        return jsonify({"error": "Item ID already exists"}), 400

    ITEM_DB[item_id] = {
        "name": data["name"],
        "slot": data["slot"],
        "quality": data["quality"],
        "dungeon": data.get("dungeon"),
        "boss": data.get("boss"),
    }

    save_item_db()
    return jsonify({"status": "ok", "id": item_id})


@items_bp.route("/items/<item_id>/edit", methods=["POST"])
def edit_item(item_id):
    if item_id not in ITEM_DB:
        return jsonify({"error": "Item not found"}), 404

    data = request.json
    item = ITEM_DB[item_id]

    for field in ["name", "slot", "quality", "dungeon", "boss"]:
        if field in data:
            item[field] = data[field]

    save_item_db()
    return jsonify({"status": "ok"})


@items_bp.route("/items/<item_id>/delete", methods=["POST"])
def delete_item(item_id):
    if item_id not in ITEM_DB:
        return jsonify({"error": "Item not found"}), 404

    del ITEM_DB[item_id]
    save_item_db()
    return jsonify({"status": "ok"})
