# API Data Integration Dashboard

A Flask and PostgreSQL project built around a realistic data integration workflow: fetch product data from an external API, normalize it, store it locally, and track synchronization history.

The goal was to practice the kind of backend workflow that actually shows up in business applications — not just "display data from an API", but the full cycle: communication with an external service, transforming raw JSON into a controlled internal format, preventing duplicates across repeated runs, and logging what happened so the process is observable.

---

## Project Status

**Stage:** backend/data integration MVP — working and testable locally.

The core synchronization workflow is implemented and running. The next layer — dashboard templates, product list UI, and frontend styling — is prepared as placeholder files and will be implemented next.

### Implemented

- Flask application structure and route setup
- PostgreSQL configuration via environment variables (`python-dotenv`)
- PostgreSQL connection test route
- Integration with DummyJSON Products API
- Product data normalization from raw API response
- PostgreSQL schema for products and synchronization logs
- Upsert logic using `ON CONFLICT (external_id) DO UPDATE`
- Manual synchronization endpoint
- Synchronization logging for both success and failure states
- Database helper for fetching the latest synchronization log
- Preview endpoint for inspecting normalized API data before saving
- `requirements.txt` and `.env.example` for local setup

### In Progress / Planned

- Dashboard UI with product statistics
- Product list page with Jinja2 templates
- Search by product title
- Category filtering
- Frontend styling
- Unit tests for normalization and database logic
- Architecture documentation
- Docker and deployment configuration

---

## Why This Project

I wanted to build something that goes beyond the typical "call an API, render the response" tutorial pattern.

Most business applications that deal with external data need to do more: import it on a schedule, transform it into their own internal format, avoid re-inserting the same records, and know whether the last import actually worked. This project is a small but complete version of that workflow.

```text
DummyJSON Products API
        ↓
Python requests
        ↓
JSON response
        ↓
Product normalization
        ↓
PostgreSQL products table
        ↓
Upsert by external_id
        ↓
Synchronization log
        ↓
Future dashboard / reporting layer
```

---

## Tech Stack

- **Python 3**
- **Flask**
- **PostgreSQL**
- **psycopg2-binary**
- **requests**
- **python-dotenv**
- **HTML / CSS** — planned for dashboard layer
- **Git / GitHub**

---

## Core Features

### External API Integration

The application fetches product data from the DummyJSON Products API:

```
https://dummyjson.com/products?limit=0
```

The request is handled in `services/api_client.py` with a timeout configured, so API failures are caught at the request level and don't break the synchronization flow silently.

### Product Data Normalization

Raw API objects contain a lot of fields the application doesn't need. The normalization step extracts only the relevant fields and maps them into a consistent internal structure:

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

This keeps the local database decoupled from whatever the external API returns. If the API adds or changes fields, the normalization layer absorbs that — the products table stays stable.

### Upsert Logic

The project uses `ON CONFLICT (external_id) DO UPDATE` to handle repeated synchronizations cleanly:

- if a product doesn't exist yet — insert it,
- if it already exists — update the relevant fields,
- running synchronization multiple times leaves the database consistent, not full of duplicates.

### Synchronization Logging

Every synchronization run writes a record to `sync_logs` — status, message, number of records processed, and timestamp. This makes it possible to answer basic operational questions without digging into database internals:

- Did the last sync succeed?
- How many records were imported?
- When did it run?

---

## API Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Health check — confirms the app is running. |
| `/db-test` | GET | Tests the PostgreSQL connection. |
| `/sync-preview` | GET | Fetches and normalizes API data, returns a sample without saving anything. |
| `/sync` | GET | Full synchronization — fetch, normalize, upsert, log results. |

---

## Database Schema

### `products`

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

## Design Decisions

### PostgreSQL over SQLite

SQLite would have been simpler to set up, but it hides too much. I wanted to work with real constraints, proper upsert syntax, and `psycopg2` directly — without an ORM abstracting away what the queries actually do.

### psycopg2 over SQLAlchemy

Same reasoning. At this stage, writing raw SQL and handling the cursor manually teaches more than letting an ORM generate queries. SQLAlchemy makes sense when a project grows — not as a starting point when the goal is to understand the database layer.

### Why store data locally instead of hitting the API on every request?

The API is fine for a demo, but the application is built around the assumption that external services are unreliable or slow. Importing data once, storing it locally, and querying the local database is a more realistic pattern for reporting tools and internal dashboards.

### Why `external_id`?

The local database has its own primary key (`id`). `external_id` stores the original product ID from the API and is marked `UNIQUE` — this is what makes upsert possible. Without it, there's no reliable way to detect whether a product already exists in the database.

---

## Project Structure

```text
api-data-integration-dashboard/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── database/
│   ├── db.py
│   └── schema.sql
├── services/
│   └── api_client.py
├── templates/
│   ├── base.html
│   ├── index.html          # planned dashboard
│   └── products.html       # planned product list
├── static/
│   └── style.css
└── docs/
    └── architecture.md     # planned
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/macus450-crypto/api-data-integration-dashboard.git
cd api-data-integration-dashboard
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`:

```env
DB_HOST=localhost
DB_NAME=api_dashboard_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_PORT=5432
```

### 5. Create the database and run the schema

```bash
psql -U postgres -c "CREATE DATABASE api_dashboard_db;"
psql -U postgres -d api_dashboard_db -f database/schema.sql
```

### 6. Run the application

```bash
python app.py
```

Available at `http://127.0.0.1:5000`.

---

## Testing the Workflow Manually

Once the app is running, the full backend workflow can be tested through the browser, Postman, or curl.

**1. Check the app is running**
```
GET /
→ "API Data Integration Dashboard is running!"
```

**2. Verify the database connection**
```
GET /db-test
→ success message with PostgreSQL connection info
```

**3. Preview normalized data without saving**
```
GET /sync-preview
→ product count + sample normalized records
```

**4. Run synchronization**
```
GET /sync
→ {"success": true, "message": "Products synchronized successfully", "records_imported": 194}
```

**5. Verify directly in PostgreSQL**

```sql
-- Check import count
SELECT COUNT(*) FROM products;

-- Check recent sync history
SELECT status, message, records_imported, created_at
FROM sync_logs
ORDER BY created_at DESC
LIMIT 5;

-- Products that need attention (low stock)
SELECT title, brand, stock
FROM products
WHERE stock < 10
ORDER BY stock ASC;

-- Category breakdown
SELECT category, COUNT(*) AS total, ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY category
ORDER BY total DESC;
```

---

## Current Limitations

- Local MVP only — no deployment configuration yet.
- Template and static files are present as placeholders; the dashboard UI is not implemented yet.
- Synchronization is triggered manually through the `/sync` endpoint.
- Error handling covers the main failure paths but isn't exhaustive.
- No authentication.
- No automated tests yet.

---

## Roadmap

**Next:**
- Dashboard homepage with product stats (total products, categories, average price, low-stock count, last sync status)
- Product list page with search and category filtering
- Basic frontend styling

**Later:**
- Pagination and sorting
- Charts for category distribution, price ranges, stock levels
- Unit tests for normalization and database functions
- Docker support
- Scheduled synchronization
