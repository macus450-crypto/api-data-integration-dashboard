# API Data Integration Dashboard

A small backend-oriented data integration dashboard built with **Python, Flask and PostgreSQL**.

The application imports product data from an external API, normalizes the received JSON response, stores records in a relational database, logs synchronization results and presents the data in a simple web dashboard.

The goal of this project is not to build a large production system, but to demonstrate a realistic junior developer workflow: working with an external API, processing data, using SQL, handling synchronization logic, documenting technical decisions and maintaining a clean Git workflow.

---

## Overview

API Data Integration Dashboard is a small project focused on practical backend and data-integration skills.

The main data flow is:

```text
DummyJSON Products API
→ Python requests
→ JSON response
→ product data normalization
→ PostgreSQL
→ synchronization logs
→ Flask routes
→ HTML dashboard
```

The project uses product data instead of generic sample data because products, categories, prices, ratings and stock levels are closer to real business workflows such as e-commerce, inventory monitoring and marketplace data management.

This project should be understood as a **Product Data Integration Dashboard**, not as a simple API table viewer.

---

## Why This Project Matters

This project was built to practice a realistic data workflow:

- fetching data from an external API,
- validating and normalizing JSON data,
- storing records in a relational database,
- preventing duplicate records,
- updating existing records during synchronization,
- logging synchronization attempts,
- displaying product data in a dashboard,
- adding search, filters and basic statistics,
- documenting architecture and technical decisions.

The main value of the project is the full workflow:

```text
External Product API → PostgreSQL → sync logs → dashboard analytics
```

The project is intentionally small, but it is designed to show practical understanding of API integration, SQL, backend logic, documentation and Git workflow.

---

## Features

### Implemented

- basic Flask application setup,
- project structure prepared,
- Git repository initialized,
- initial application route.

### Planned MVP Features

- external Product API integration,
- JSON data processing,
- product data normalization,
- PostgreSQL database connection,
- product data storage,
- duplicate prevention during synchronization,
- updating existing products during repeated imports,
- synchronization logs,
- basic dashboard statistics,
- searchable product list,
- filtering by category,
- product price, rating and stock analysis,
- simple HTML/CSS interface,
- technical documentation.

---

## Tech Stack

- Python 3
- Flask
- PostgreSQL
- psycopg2-binary
- requests
- python-dotenv
- HTML
- CSS
- Git
- GitHub

---

## Current Status

The project is currently in the early development stage.

Completed:

- project directory created,
- Python virtual environment configured,
- required dependencies installed,
- initial Flask application created,
- project structure prepared,
- Git repository initialized,
- initial commit created,
- project pushed to GitHub.

Current focus:

- replacing the initial country-data concept with product data,
- configuring PostgreSQL,
- creating the product database schema,
- preparing synchronization logs,
- connecting the application to the database.

Next steps:

- implement DummyJSON Products API integration,
- normalize product data,
- save products to PostgreSQL,
- add insert/update synchronization logic,
- create dashboard views,
- add product search and category filtering,
- document architecture and technical decisions.

---

## Project Structure

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

> Note: if the project still contains `templates/countries.html`, it should be renamed to `templates/products.html` to keep the project consistent with the product-data domain.

---

## External API

The project uses:

```text
DummyJSON Products API
```

Example endpoint:

```text
https://dummyjson.com/products
```

The API provides product-like data suitable for a small dashboard:

- product title,
- brand,
- category,
- price,
- discount percentage,
- rating,
- stock,
- thumbnail image.

The application should not use the raw API response directly in templates. Data should first be normalized into a controlled internal format.

Example normalized product:

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

---

## Database Schema

The project uses two main tables:

- `products`
- `sync_logs`

### `products`

Stores normalized product data fetched from the external API.

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

### `sync_logs`

Stores synchronization history.

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

## Data Synchronization

The synchronization process should follow this flow:

```text
1. User triggers synchronization.
2. Flask calls the API client.
3. The API client fetches product data from DummyJSON.
4. The response status is checked.
5. JSON data is normalized.
6. Products are inserted or updated in PostgreSQL.
7. The synchronization result is saved in sync_logs.
8. The dashboard displays the latest synchronization status.
```

The application should avoid duplicate records by using `external_id` as a unique identifier.

Expected logic:

```text
if product exists → update existing record
if product does not exist → insert new record
```

In PostgreSQL, this can later be handled with `ON CONFLICT (external_id) DO UPDATE`.

---

## Dashboard Scope

The dashboard should show more than a simple product table.

Planned dashboard cards:

- total number of products,
- number of categories,
- average product price,
- number of low-stock products,
- last synchronization status,
- last synchronization date,
- number of records processed during last synchronization.

The `/products` page should include:

- product list,
- search by product title,
- filter by category,
- product price,
- product rating,
- stock level,
- optional sorting by price, rating or stock.

---

## Example SQL Queries

```sql
SELECT * FROM products;

SELECT COUNT(*) FROM products;

SELECT * FROM products
WHERE category = 'smartphones';

SELECT * FROM products
ORDER BY price DESC;

SELECT * FROM products
ORDER BY rating DESC;

SELECT * FROM products
WHERE stock < 10;

SELECT category, COUNT(*) AS product_count
FROM products
GROUP BY category;

SELECT AVG(price) AS average_price
FROM products;
```

These queries are the foundation for the dashboard statistics, search and filtering features.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/macus450-crypto/api-data-integration-dashboard.git
```

Go to the project directory:

```bash
cd api-data-integration-dashboard
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows CMD:

```bash
venv\Scripts\activate.bat
```

Or on Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the application in the browser:

```text
http://127.0.0.1:5000
```

---

## Environment Configuration

The project uses environment variables for database configuration.

Example `.env` file:

```env
DB_NAME=api_dashboard_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

The real `.env` file should not be committed to the repository.

Use `.env.example` to document required configuration values.

---

## Technical Notes

The application follows a simple structure:

- `app.py` contains Flask routes,
- `services/api_client.py` handles communication with the external Product API,
- `database/db.py` handles database operations,
- `database/schema.sql` contains SQL table definitions,
- `templates/` contains HTML views,
- `static/` contains CSS,
- `docs/` contains technical documentation.

The goal is to keep the project small, readable and easy to extend.

---

## Key Technical Decisions

### Why PostgreSQL?

PostgreSQL was selected to practice working with a real relational database, SQL queries, unique records and persistent storage instead of keeping API data only in memory or JSON files.

### Why store API data in the database?

The application simulates a real integration workflow where external data is imported, normalized and stored locally. This allows the dashboard to work with stable database records instead of depending on the external API on every page load.

### Why use `sync_logs`?

Synchronization should be observable. The `sync_logs` table makes it possible to track when synchronization happened, whether it succeeded and how many records were processed.

### Why use `external_id`?

`external_id` identifies a product from the external API. It allows the application to prevent duplicates and update existing records during repeated synchronizations.

### Why keep the MVP small?

The purpose of the project is to demonstrate practical backend, API, SQL and documentation skills in a focused scope. Advanced features such as authentication, deployment, Docker or a complex frontend are outside the current MVP scope.

---

## Error Handling

The project should handle expected failure cases, including:

- external API not responding,
- external API returning an unexpected status code,
- unexpected JSON structure,
- missing product fields,
- database connection error,
- failed insert/update operation,
- empty dataset.

In case of synchronization failure, the application should not crash silently. It should save an error entry in `sync_logs` and show a clear message to the user.

---

## Known Limitations

- The application currently runs locally.
- PostgreSQL setup is local and depends on environment variables.
- Synchronization is triggered manually.
- Authentication is not included.
- Deployment is outside the current MVP scope.
- The dashboard is intentionally simple and focused on backend/data workflow.
- The project uses a public demo Product API, not a real marketplace API.

---

## Future Improvements

Possible improvements:

- add sorting by price, rating and stock,
- add pagination for product lists,
- add better dashboard charts,
- add product detail pages,
- add automated synchronization,
- add tests for data normalization,
- add more advanced error logging,
- deploy the application,
- replace the demo API with a more realistic data source,
- add Docker after the MVP is stable.



