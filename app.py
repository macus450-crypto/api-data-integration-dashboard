from flask import Flask
from database.db import test_connection
from services.api_client import fetch_products

app = Flask(__name__)


@app.route("/")
def index():
    return "API Data Integration Dashboard is running!"


@app.route("/db-test")
def db_test():
    result = test_connection()

    if result["success"]:
        return result["message"], 200

    return result["message"], 500

@app.route("/sync-preview")
def sync_preview():
    products = fetch_products()

    return {
        "products_count": len(products),
        "sample_products": products[:5]
    }


if __name__ == "__main__":
    app.run(debug=True)