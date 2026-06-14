from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

from config import Config
from models import Item, db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        query = Item.query
        category = request.args.get("category")
        if category:
            query = query.filter_by(category=category)

        items = query.order_by(Item.name).all()
        categories = sorted({i.category for i in Item.query.all() if i.category})

        return render_template(
            "index.html", items=items, categories=categories, selected_category=category
        )

    @app.route("/items/new", methods=["GET", "POST"])
    def add_item():
        if request.method == "POST":
            item = Item(
                name=request.form["name"].strip(),
                category=request.form.get("category", "").strip() or None,
                quantity=float(request.form.get("quantity") or 0),
                unit=request.form.get("unit", "").strip() or None,
                low_stock_threshold=float(request.form.get("low_stock_threshold") or 1),
                expiration_date=_parse_date(request.form.get("expiration_date")),
                notes=request.form.get("notes", "").strip() or None,
            )
            db.session.add(item)
            db.session.commit()
            flash(f"Added {item.name}.", "success")
            return redirect(url_for("index"))

        return render_template("item_form.html", item=None)

    @app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
    def edit_item(item_id):
        item = Item.query.get_or_404(item_id)

        if request.method == "POST":
            item.name = request.form["name"].strip()
            item.category = request.form.get("category", "").strip() or None
            item.quantity = float(request.form.get("quantity") or 0)
            item.unit = request.form.get("unit", "").strip() or None
            item.low_stock_threshold = float(request.form.get("low_stock_threshold") or 1)
            item.expiration_date = _parse_date(request.form.get("expiration_date"))
            item.notes = request.form.get("notes", "").strip() or None

            db.session.commit()
            flash(f"Updated {item.name}.", "success")
            return redirect(url_for("index"))

        return render_template("item_form.html", item=item)

    @app.route("/items/<int:item_id>/delete", methods=["POST"])
    def delete_item(item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        flash(f"Removed {item.name}.", "success")
        return redirect(url_for("index"))

    @app.route("/items/<int:item_id>/adjust", methods=["POST"])
    def adjust_quantity(item_id):
        item = Item.query.get_or_404(item_id)
        delta = float(request.form.get("delta", 0))
        item.quantity = max(0, item.quantity + delta)
        db.session.commit()
        return redirect(url_for("index"))

    return app


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config.get("FLASK_DEBUG", True))
