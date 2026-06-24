from flask import Flask, render_template, request
from database.db import test_connection, save_product, save_sync_log, get_dashboard_stats, get_products, get_categories
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
    fetch_result = fetch_products()
    
    if fetch_result["success"] == False:
        return {
            "success": False,
            "status": "error",
            "message": fetch_result.get("message"),
            "products_count": 0,
            "sample_products": []
        }, 500
    
    products = fetch_result.get("products", [])

    return {
        "success": True,
        "status": "success",
        "message": fetch_result.get("message"),
        "products_count": len(products),
        "sample_products": products[:5]
    }

@app.route("/sync")
def sync_products():
    fetch_result = fetch_products()
    
    if fetch_result["success"] == False:
        save_sync_log(
            "error",
            fetch_result.get("message"),
            0
        )
        return {
            "success": False,
            "status": "error",
            "message": fetch_result.get("message"),
            "records_imported": 0
        }, 500
        

    products = fetch_result.get("products", [])

    if not products:
        save_sync_log(
            "error",
            "No products fetched from external API",
            0
        )
        return {
            "success": False,
            "status": "error",
            "message": "No products fetched from external API",
            "records_imported": 0
        }, 500
    
    imported_count = 0
    not_imported_count = 0
    
    for product in products:
        result = save_product(product) 
        if result["success"]: 
            imported_count += 1
        else:
            not_imported_count += 1
    
    if not_imported_count == 0:
        save_sync_log(
            "success",
            "Products synchronized successfully",
            imported_count
        )
        return {
            "success": True,
            "status": "success",
            "message": "Products synchronized successfully",
            "records_imported": imported_count,
            "records_not_imported": not_imported_count
        }
    else:
        save_sync_log(
            "partial_success",
            f"Products synchronized with some errors. Imported: {imported_count}, Not Imported: {not_imported_count}",
            imported_count,
        )
        return {
            "success": True,
            "status": "partial_success",
            "message": f"Products synchronized with some errors. Imported: {imported_count}, Not Imported: {not_imported_count}",
            "records_imported": imported_count,
            "records_not_imported": not_imported_count
        }

@app.route("/products")
def products():
    search = request.args.get("search")
    category = request.args.get("category")
    
    categories = get_categories()
    products_list = get_products(search=search, category=category)
    return render_template("products.html", products=products_list, search=search, category=category, categories=categories)

if __name__ == "__main__":
    app.run(debug=True)