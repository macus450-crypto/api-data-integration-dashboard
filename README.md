# API Data Integration Dashboard

API Data Integration Dashboard is a small Flask and PostgreSQL project focused on external API integration, product data normalization, database persistence, synchronization logging, and basic dashboard analytics.

The application is designed as a practical junior developer project. Its goal is not to be a large production system, but to demonstrate a clear backend/data workflow: fetch product data from an external API, normalize it, store it in a relational database, prevent duplicates, log synchronization attempts, and present the results in a simple web dashboard.

---

## Project Status

This project is currently in active development.

### Implemented

- Basic Flask application setup
- Initial project structure
- Virtual environment configuration
- Git repository initialization
- Basic root route for local development

### Planned MVP Features

- Integration with DummyJSON Products API
- Product data normalization
- PostgreSQL database connection
- `products` table for normalized product records
- `sync_logs` table for synchronization history
- Duplicate prevention using external product IDs
- Insert/update logic during repeated synchronizations
- Dashboard with product statistics
- Product list page
- Search by product name
- Filter by category
- Basic price, rating, and stock analysis
- Error handling for API and database issues
- Technical documentation

---

## Why This Project Matters

This project was built to practice a realistic backend/data workflow often found in business applications:

```text
External Product API
→ Python requests
→ JSON response
→ product data normalization
→ PostgreSQL
→ synchronization logs
→ Flask dashboard
→ search, filtering and statistics
```

The main focus is not simply displaying products from an API. The focus is the full data integration process: communication with an external service, transforming raw JSON into a controlled internal format, storing it in a relational database, tracking synchronization results, and presenting the data in a clear dashboard.

---

## Tech Stack

- Python 3
- Flask
- PostgreSQL
- SQL
- psycopg2-binary
- requests
- python-dotenv
- HTML
- CSS
- Git
- GitHub

---

## External API

The project uses DummyJSON Products API as the external data source.

Example endpoint:

```text
https://dummyjson.com/products
```

The API provides product-like data that can be used to simulate a small e-commerce-style data workflow. The application focuses on selected fields such as product title, brand, category, price, discount, rating, stock level, and thumbnail URL.

---

## Core Features

### Product Synchronization

The application is planned to fetch product data from an external API and store it locally in PostgreSQL.

Synchronization flow:

```text
1. The user triggers synchronization.
2. Flask calls the external Product API.
3. The API returns JSON data.
4. The application validates and normalizes selected fields.
5. Products are inserted or updated in PostgreSQL.
6. Synchronization result is saved in sync_logs.
7. The dashboard displays the latest synchronization status.
```

### Product Data Normalization

Raw API responses are transformed into a simpler internal structure before being saved to the database.

Example normalized product structure:

```python
{
    "external_id": 1,
    "title": "Essence Mascara Lash Princess",
    "brand": "Essence",
    "category": "beauty",
    "price": 9.99,
    "discount_percentage": 7.17,
    "rating": 4.94,
    "stock": 5,
    "thumbnail_url": "https://example.com/image.png"
}
```

### Dashboard

The dashboard is planned to show a quick overview of the imported product data.

Planned dashboard metrics:

- Total number of products
- Number of product categories
- Average product price
- Number of low-stock products
- Last synchronization status
- Last synchronization date
- Number of records processed during the last synchronization

### Product List

The product list page is planned to include:

- Product title
- Brand
- Category
- Price
- Discount percentage
- Rating
- Stock level
- Search by product name
- Filter by category

---

## Database Schema

The project uses PostgreSQL to store normalized product data and synchronization history.

### `products` table

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    external_id INTEGER UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    brand VARCHAR(255),
    category VARCHAR(100),
    price NUMERIC(10, 2),
    discount_percentage NUMERIC(5, 2),
    rating NUMERIC(3, 2),
    stock INTEGER,
    thumbnail_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### `sync_logs` table

```sql
CREATE TABLE sync_logs (
    id SERIAL PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    message TEXT,
    records_imported INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Database Design Decisions

### Why PostgreSQL?

PostgreSQL was selected to practice working with a relational database, SQL queries, unique constraints, persistent data storage, and structured backend development.

### Why store API data locally?

The project simulates a common integration workflow where data from an external source is imported, normalized, stored, and later queried locally instead of being fetched from the external API on every page load.

### Why use `external_id`?

`external_id` stores the product ID from the external API. It is marked as `UNIQUE` so the application can recognize existing products and avoid duplicate records during repeated synchronizations.

### Why use `sync_logs`?

Synchronization logs make the import process easier to monitor and debug. They allow the application to track whether synchronization succeeded, how many records were processed, and when the last synchronization happened.

---

## Example SQL Queries

These queries are planned to support the dashboard, filtering, and basic product analysis.

```sql
SELECT * FROM products;
```

```sql
SELECT COUNT(*) FROM products;
```

```sql
SELECT * FROM products
WHERE category = 'smartphones';
```

```sql
SELECT * FROM products
ORDER BY price DESC;
```

```sql
SELECT * FROM products
ORDER BY rating DESC;
```

```sql
SELECT * FROM products
WHERE stock < 10;
```

```sql
SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category;
```

```sql
SELECT AVG(price) AS average_price
FROM products;
```

---

## Project Structure

Planned structure:

```text
api-data-integration-dashboard/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── templates/
│   ├── base.html
│   ├── index.html
│   └── products.html
├── static/
│   └── style.css
├── services/
│   └── api_client.py
├── database/
│   ├── db.py
│   └── schema.sql
└── docs/
    └── architecture.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/macus450-crypto/api-data-integration-dashboard.git
cd api-data-integration-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
DB_NAME=api_dashboard_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run the application

```bash
python app.py
```

The application should be available at:

```text
http://127.0.0.1:5000
```

---

## Usage

Current development route:

```text
/
```

Planned routes:

```text
/              Dashboard overview
/products      Product list with search and category filtering
/sync          Synchronize product data from external API
/sync-preview  Preview external API data before saving it to the database
```

---

## Error Handling Goals

The project is planned to handle common integration and database issues, including:

- External API not responding
- Unexpected API status code
- Invalid or unexpected JSON structure
- Missing product fields
- Database connection failure
- Failed insert/update operation
- Empty data state in the dashboard

If synchronization fails, the application should not crash without control. It should save an error entry in `sync_logs` and display a clear message to the user.

---

## Known Limitations

- The project is currently designed as a local MVP.
- User authentication is not included.
- Synchronization is planned to be triggered manually.
- The project does not include deployment configuration yet.
- The dashboard focuses on basic statistics rather than advanced analytics.
- The external API is used for learning and development purposes, not as a production data source.

---

## Future Improvements

Possible future improvements include:

- Pagination for product list
- Sorting by price, rating, and stock
- More advanced dashboard charts
- Product detail page
- Better validation layer
- Automated synchronization schedule
- Unit tests for data normalization
- Deployment configuration
- Docker support
- More detailed architecture documentation

---

## Project Summary

API Data Integration Dashboard is a small backend/data project built with Python, Flask, and PostgreSQL. It is focused on importing product data from an external API, normalizing it, storing it in a relational database, logging synchronization results, and presenting basic product analytics through a simple dashboard.
