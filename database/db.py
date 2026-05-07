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