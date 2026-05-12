import requests


def fetch_products():
    url = "https://dummyjson.com/products?limit=0"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        normalized_products = []

        for product in products:
            normalized_product = {
                "external_id": product.get("id"),
                "title": product.get("title"),
                "brand": product.get("brand"),
                "category": product.get("category"),
                "price": product.get("price"),
                "discount_percentage": product.get("discountPercentage"),
                "rating": product.get("rating"),
                "stock": product.get("stock"),
                "thumbnail_url": product.get("thumbnail"),
            }

            normalized_products.append(normalized_product)

        return normalized_products

    except requests.exceptions.RequestException as error:
        print(f"Error while fetching products: {error}")
        return []