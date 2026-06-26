from flask import Blueprint, render_template, request, redirect, url_for
from ..db import db

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/manage_accounts")
def manage_accounts():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts ORDER BY name")
    accounts = cur.fetchall()
    conn.close()
    return render_template("manage_accounts.html", accounts=accounts)


@accounts_bp.route("/add_account", methods=["POST"])
def add_account():
    name = request.form["name"]
    conn = db()
    conn.execute("INSERT INTO accounts (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return redirect(url_for("accounts.manage_accounts"))


@accounts_bp.route("/delete_account/<int:account_id>", methods=["POST"])
def delete_account(account_id):
    conn = db()
    conn.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("accounts.manage_accounts"))
