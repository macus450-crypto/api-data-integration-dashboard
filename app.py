from flask import Flask, render_template
from database.db import test_connection, save_product, save_sync_log, get_dashboard_stats, get_products
from services.api_client import fetch_products

app = Flask(__name__)


@app.route("/")
def index():
    stats = get_dashboard_stats()
    return render_template("index.html", stats=stats)


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

@app.route("/sync")
def sync_products():
    products = fetch_products()

    if not products:
        save_sync_log(
            "error",
            "No products fetched from external API",
            0
        )
        return {
            "success": False,
            "message": "No products fetched from external API",
            "records_imported": 0
        }, 500
    
    imported_count = 0
    
    for product in products:
        result = save_product(product) 
        if result["success"]: 
            imported_count += 1

    save_sync_log(
        "success",
        "Products synchronized successfully",
        imported_count
    )
    return {
        "success": True,
        "message": "Products synchronized successfully",
        "records_imported": imported_count
    }

@app.route("/products")
def products():
    products_list = get_products()
    return render_template("products.html", products=products_list)

if __name__ == "__main__":
    app.run(debug=True)