from flask import Flask, render_template, request, redirect, url_for, flash
from config import SECRET_KEY
from database.db import (
    test_connection,
    save_product,
    save_sync_log,
    get_dashboard_stats,
    get_products,
    get_products_count,
    get_categories,
)
from services.api_client import fetch_products

app = Flask(__name__)
app.secret_key = SECRET_KEY

PRODUCTS_PER_PAGE = 20

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

    if not fetch_result["success"]:
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

@app.route("/sync", methods=["POST"])
def sync_products():
    fetch_result = fetch_products()

    if not fetch_result["success"]:
        message = fetch_result.get("message")
        save_sync_log(
            "error",
            message,
            0
        )
        flash(message, "error")
        return redirect(url_for("index"))

    products = fetch_result.get("products", [])

    if not products:
        message = "No products fetched from external API"
        save_sync_log(
            "error",
            message,
            0
        )
        flash(message, "error")
        return redirect(url_for("index"))

    imported_count = 0
    not_imported_count = 0

    for product in products:
        result = save_product(product)
        if result["success"]:
            imported_count += 1
        else:
            not_imported_count += 1

    if not_imported_count == 0:
        message = f"Products synchronized successfully. Imported: {imported_count}"
        save_sync_log(
            "success",
            message,
            imported_count
        )
        flash(message, "success")
        return redirect(url_for("index"))

    message = f"Products synchronized with some errors. Imported: {imported_count}, Not Imported: {not_imported_count}"
    save_sync_log(
        "partial_success",
        message,
        imported_count,
    )
    flash(message, "warning")
    return redirect(url_for("index"))

@app.route("/products")
def products():
    search = request.args.get("search")
    category = request.args.get("category")
    page = request.args.get("page", 1, type=int)

    categories = get_categories()
    total_products = get_products_count(search=search, category=category)
    total_pages = max((total_products + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE, 1)

    if page is None or page < 1:
        page = 1

    if page > total_pages:
        page = total_pages

    offset = (page - 1) * PRODUCTS_PER_PAGE
    products_list = get_products(
        search=search,
        category=category,
        limit=PRODUCTS_PER_PAGE,
        offset=offset,
    )

    start_item = offset + 1 if total_products else 0
    end_item = offset + len(products_list)

    filter_args = {}
    if search:
        filter_args["search"] = search
    if category:
        filter_args["category"] = category

    prev_url = url_for("products", page=page - 1, **filter_args) if page > 1 else None
    next_url = url_for("products", page=page + 1, **filter_args) if page < total_pages else None

    return render_template(
        "products.html",
        products=products_list,
        search=search,
        category=category,
        categories=categories,
        page=page,
        total_pages=total_pages,
        total_products=total_products,
        start_item=start_item,
        end_item=end_item,
        prev_url=prev_url,
        next_url=next_url,
    )

if __name__ == "__main__":
    app.run(debug=True)
