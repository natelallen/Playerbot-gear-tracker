from flask import Flask
from pathlib import Path

from .db import init_db
from .item_db import load_item_db

def create_app():
    app = Flask(__name__)

    # Ensure DB exists
    if not Path("data/database.db").exists():
        init_db()

    # Load JSON item DB once
    load_item_db()

    from .routes.dashboard import dashboard_bp
    from .routes.accounts import accounts_bp
    from .routes.characters import characters_bp
    from .routes.wishlist import wishlist_bp
    from .routes.presets import presets_bp
    from .routes.items import items_bp
    from .routes.dungeons import dungeons_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(characters_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(presets_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(dungeons_bp)

    return app
