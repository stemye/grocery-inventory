import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://localhost:5432/grocery_inventory"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
