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

def save_sync_log(status, message, records_imported):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO sync_logs (
                status,
                message,
                records_imported
            )
            VALUES (%s, %s, %s);
        """

        values = (
            status,
            message,
            records_imported
        )

        cursor.execute(query, values)
        connection.commit()

        return {
            "success": True,
            "message": "Sync log saved successfully"
        }

    except Exception as error:
        if connection:
            connection.rollback()

        return {
            "success": False,
            "message": f"Failed to save sync log: {error}"
        }

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_last_sync_log():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT status, message, records_imported, created_at
            FROM sync_logs
            ORDER BY created_at DESC
            LIMIT 1;
        """

        cursor.execute(query)
        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "status": row[0],
            "message": row[1],
            "records_imported": row[2],
            "created_at": row[3]
        }

    except Exception as error:
        return {
            "status": "error",
            "message": f"Failed to fetch last sync log: {error}",
            "records_imported": 0,
            "created_at": None
        }

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_dashboard_stats():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS total_products,
                COUNT(DISTINCT category) AS categories_count,
                COALESCE(ROUND(AVG(price)::numeric, 2), 0) AS average_price,
                COUNT(*) FILTER (WHERE stock < 10) AS low_stock_products
            FROM products;
        """)

        stats_row = cursor.fetchone()

        total_products = stats_row[0]
        categories_count = stats_row[1]
        average_price = stats_row[2]
        low_stock_products = stats_row[3]

        cursor.execute("""
            SELECT status, message, records_imported, created_at
            FROM sync_logs
            ORDER BY created_at DESC
            LIMIT 1;
        """)

        last_sync_row = cursor.fetchone()

        if last_sync_row:
            last_sync = {
                "status": last_sync_row[0],
                "message": last_sync_row[1],
                "records_imported": last_sync_row[2],
                "created_at": last_sync_row[3],
            }
        else:
            last_sync = None

        return {
            "total_products": total_products,
            "categories_count": categories_count,
            "average_price": float(average_price),
            "low_stock_products": low_stock_products,
            "last_sync": last_sync,
        }

    except Exception as error:
        return {
            "total_products": 0,
            "categories_count": 0,
            "average_price": 0,
            "low_stock_products": 0,
            "last_sync": None,
            "error": f"Failed to get dashboard stats: {error}"
        }

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_products(search=None, category=None):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        conditions = []
        parameters = []

        query = """
            SELECT title, brand, category, price, discount_percentage, rating, stock
            FROM products
        """

        if search:
            conditions.append("(title ILIKE %s OR brand ILIKE %s OR category ILIKE %s)")
            
            search_value = f"%{search}%"
            
            parameters.extend([search_value, search_value, search_value])
        
        if category:
            conditions.append("(category = %s)")
            
            parameters.append(category)

        if conditions:
            query += "WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY title ASC;"

        cursor.execute(query, parameters)

        rows = cursor.fetchall()

        products = []
        
        for row in rows:
            product = {
                "title": row[0],
                "brand": row[1],
                "category": row[2],
                "price": row[3],
                "discount_percentage": row[4],
                "rating": row[5],
                "stock": row[6]
            }

            products.append(product)
        
        return products

    except Exception as error:
        print(f"Failed to get products: {error}")
    
        return []
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_categories():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        SELECT DISTINCT category
        FROM products
        WHERE category IS NOT NULL
        ORDER BY category ASC;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        categories_list = []

        for row in rows:
            categories_list.append(row[0])

        return categories_list

    
    except Exception as error:
        
        print(f"Failed to get categories: {error}")
        
        return []
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
