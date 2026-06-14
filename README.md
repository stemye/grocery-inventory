# Grocery Inventory

A simple home grocery inventory tracker built with Flask and PostgreSQL.

## Features

- Add, edit, and delete grocery items
- Track quantity, unit, category, and expiration date
- Quick +/- buttons to adjust quantity as you use items
- Low-stock and expiring-soon highlights
- Filter items by category

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create a PostgreSQL database:

   ```bash
   createdb grocery_inventory
   ```

3. Copy `.env.example` to `.env` and set your database connection string and secret key:

   ```bash
   cp .env.example .env
   ```

4. Run the app:

   ```bash
   python app.py
   ```

   The app creates its tables automatically on first run and is available at
   http://localhost:5000.

## Deploying

This app works well on DigitalOcean's App Platform with a Managed PostgreSQL
database — just set the `DATABASE_URL` environment variable to your managed
database's connection string.

## Project structure

```
app.py          - routes and app factory
models.py       - SQLAlchemy models (Item)
config.py       - configuration from environment variables
templates/      - Jinja templates
static/         - CSS
```

## Roadmap ideas

- Barcode scanning to add items quickly
- Shopping list generation from low-stock items
- Multi-user / household support
- Mobile-friendly UI improvements
