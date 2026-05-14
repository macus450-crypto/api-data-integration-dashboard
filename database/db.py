import psycopg2
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def test_connection():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()

        cursor.close()
        connection.close()

        return {
            "success": True,
            "message": f"Connected to PostgreSQL: {db_version[0]}"
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Database connection failed: {error}"
        }
    
def save_product(product):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO products (
                external_id,
                title,
                brand,
                category,
                price,
                discount_percentage,
                rating,
                stock,
                thumbnail_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (external_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                brand = EXCLUDED.brand,
                category = EXCLUDED.category,
                price = EXCLUDED.price,
                discount_percentage = EXCLUDED.discount_percentage,
                rating = EXCLUDED.rating,
                stock = EXCLUDED.stock,
                thumbnail_url = EXCLUDED.thumbnail_url,
                updated_at = CURRENT_TIMESTAMP;
        """

        values = (
            product["external_id"],
            product["title"],
            product["brand"],
            product["category"],
            product["price"],
            product["discount_percentage"],
            product["rating"],
            product["stock"],
            product["thumbnail_url"]
        )

        cursor.execute(query, values)
        connection.commit()

        return {
            "success": True,
            "message": "Product save successfully"
        }
    except Exception as error:
        if connection:
            connection.rollback()

            return {
                "success": False,
                "message": f"Failed to save product: {error}"
            }
    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()