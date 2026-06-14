from datetime import date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(60), nullable=True)
    quantity = db.Column(db.Float, nullable=False, default=0)
    unit = db.Column(db.String(30), nullable=True)  # e.g. "lbs", "boxes", "gallons"
    low_stock_threshold = db.Column(db.Float, nullable=False, default=1)
    expiration_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.String(255), nullable=True)

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    @property
    def is_expiring_soon(self):
        if not self.expiration_date:
            return False
        return (self.expiration_date - date.today()).days <= 7

    def __repr__(self):
        return f"<Item {self.name} ({self.quantity} {self.unit or ''})>"
