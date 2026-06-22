# API Data Integration Dashboard

A Flask and PostgreSQL project built around a realistic data integration workflow: fetching product data from an external API, normalizing it, storing it locally, and displaying it through a basic server-rendered dashboard.

---

## Project Status

**Stage:** local backend/data integration MVP with a basic dashboard UI — working and testable locally.

The core synchronization workflow is implemented. The project includes a Jinja2 dashboard with product statistics, last synchronization info, and a product list with search and category filtering.

The next stage is frontend structure, styling, pagination and sorting, automated tests, architecture docs, and deployment.

---

## Implemented

- Flask application structure and route setup
- PostgreSQL configuration via environment variables using `python-dotenv`
- PostgreSQL connection test route
- Integration with the DummyJSON Products API
- Product data normalization from raw API response
- PostgreSQL schema for products and synchronization logs
- Upsert logic using `ON CONFLICT (external_id) DO UPDATE`
- Manual synchronization endpoint
- Synchronization logging for both success and failure states
- Dashboard statistics: total products, number of categories, average price, low-stock count
- Latest synchronization status on the dashboard
- Product list page rendered with Jinja2
- Product search by title, brand, or category
- Category filter populated from PostgreSQL
- Preview endpoint for inspecting normalized data before saving
- `requirements.txt` and `.env.example` for local setup

---

## In Progress / Planned

- Shared base layout using `base.html`
- Frontend styling in `static/style.css`
- Pagination and sorting for the product list
- Charts for category distribution, price ranges, or stock levels
- Unit tests for normalization and database logic
- Architecture documentation in `docs/architecture.md`
- Docker support and deployment configuration
- Scheduled synchronization

---

## Why This Project

I wanted to build something closer to how external data integration actually works in backend applications — not just fetch-and-display, but import, normalize, deduplicate, store, and make queryable. The synchronization log was also something I specifically wanted to practice, since without it you have no visibility into whether the last import worked or how many records came through.

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
Dashboard statistics and product list
```

---

## Tech Stack

- Python 3
- Flask
- PostgreSQL
- psycopg2-binary
- requests
- python-dotenv
- Jinja2 templates
- HTML / CSS (styling planned)
- Git / GitHub

---

## Core Features

### External API Integration

Fetches product data from the DummyJSON Products API:

```text
https://dummyjson.com/products?limit=0
```

Handled in `services/api_client.py` with a timeout and basic error handling. If the request fails, the function returns an empty list so the rest of the sync flow doesn't crash.

### Product Data Normalization

The raw API response contains many fields that aren't needed here. Normalization pulls out only what the local schema requires:

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

This keeps the local schema stable — if the upstream API adds fields, nothing breaks on this end.

### Upsert Logic

Uses `ON CONFLICT (external_id) DO UPDATE` so repeated syncs are safe:

- new products are inserted,
- existing ones are updated,
- no duplicates accumulate.

### Synchronization Logging

Every sync writes a record to `sync_logs` with status, message, record count, and timestamp. This makes it easy to see on the dashboard whether the last import worked, and when it ran.

### Dashboard Statistics

The homepage shows basic stats pulled from the local database:

- total products
- number of unique categories
- average product price
- low-stock product count
- latest sync status

### Product List, Search, and Filtering

The `/products` page supports searching by title, brand, or category, filtering by category, and clearing active filters. Results are displayed in an HTML table. Layout and styling are still planned.

---

## API Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Dashboard homepage with product statistics and latest sync info. |
| `/db-test` | GET | Tests the PostgreSQL connection. |
| `/sync-preview` | GET | Fetches and normalizes API data, returns a sample without saving. |
| `/sync` | GET | Runs full synchronization: fetch, normalize, upsert, log. |
| `/products` | GET | Product list with optional search and category filtering. |

Example filtering:

```text
/products?search=phone
/products?category=smartphones
/products?search=phone&category=mobile-accessories
```

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

> Note: `updated_at` is set in the application layer on every update — there is no database-level trigger for it yet.

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

SQLite would have been simpler to set up, but the point of the project was to practice PostgreSQL — connections, environment config, upsert behavior, raw SQL. SQLite would have shortcut that.

### psycopg2 over SQLAlchemy

I deliberately avoided an ORM here. Writing raw SQL made it easier to understand exactly what each query does, and makes the database layer straightforward to walk through in a code review. SQLAlchemy would be a reasonable next step if the project grows more complex.

### Why store data locally instead of querying the API per request?

External APIs can be slow, rate-limited, or temporarily unavailable. Storing data locally means the dashboard always has something to query, and the application controls its own data consistency rather than depending on a third-party response being well-formed every time.

### Why `external_id`?

The local database has its own internal `id`. The `external_id` stores the original product ID from DummyJSON and is marked unique — that's what lets the upsert logic detect whether a product already exists rather than inserting a duplicate.

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
│   ├── base.html          # planned shared layout
│   ├── index.html         # dashboard page
│   └── products.html      # product list, search and category filter
├── static/
│   └── style.css          # planned styling
└── docs/
    ├── architecture.md    # planned
    └── qa/
        ├── 00-context.md
        ├── 01-current-state-review.md
        ├── 02-test-charter.md
        ├── 03-test-cases.md
        ├── 04-test-execution-log.md
        ├── 05-bug-reports-and-observations.md
        └── evidence/
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

## Manual Testing Workflow

### 1. Open the dashboard

```http
GET /
```

Dashboard with product stats and last sync info.

### 2. Verify the database connection

```http
GET /db-test
```

Success message with PostgreSQL connection info.

### 3. Preview normalized data without saving

```http
GET /sync-preview
```

Product count and a sample of normalized records.

### 4. Run synchronization

```http
GET /sync
```

Expected response:

```json
{
    "success": true,
    "message": "Products synchronized successfully",
    "records_imported": 194
}
```

### 5. Open the product list

```http
GET /products
```

Product table from PostgreSQL.

### 6. Test search and filtering

```http
GET /products?search=phone
GET /products?category=smartphones
GET /products?search=phone&category=mobile-accessories
```

### 7. Verify directly in PostgreSQL

```sql
-- Check imported product count
SELECT COUNT(*) FROM products;

-- Recent sync history
SELECT status, message, records_imported, created_at
FROM sync_logs
ORDER BY created_at DESC
LIMIT 5;

-- Products low on stock
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

## Manual QA Review

This project includes a local manual QA review focused on the main MVP data integration flow.

The QA pass covered the following areas:

* database connection
* external API preview
* manual product synchronization
* dashboard statistics
* products page
* keyword search
* category filtering
* combined search and category filtering
* empty search result behavior
* repeated synchronization and duplicate prevention

All manual test cases from TC-001 to TC-010 passed in the tested local environment.

QA documentation is available in [`docs/qa`](docs/qa):

* [`00-context.md`](docs/qa/00-context.md) - baseline notes and initial environment check
* [`01-current-state-review.md`](docs/qa/01-current-state-review.md) - current state review of implemented, partial and planned features
* [`02-test-charter.md`](docs/qa/02-test-charter.md) - scope, risks and test approach for this QA pass
* [`03-test-cases.md`](docs/qa/03-test-cases.md) - manual test cases for the main MVP flow
* [`04-test-execution-log.md`](docs/qa/04-test-execution-log.md) - executed test results with actual results and evidence references
* [`05-bug-reports-and-observations.md`](docs/qa/05-bug-reports-and-observations.md) - QA observations, limitations and recommendations

Evidence files are stored in [`docs/qa/evidence`](docs/qa/evidence), including screenshots and SQL verification for duplicate prevention.

Main QA conclusion:

The core MVP flow works as expected in the tested local environment. Products can be fetched from the external API, normalized, synchronized into PostgreSQL, displayed on the dashboard and browsed through the products page with search and category filtering.

No functional bugs were found in the main tested MVP flow during this QA pass.

The main recommended improvements are changing `/sync` from GET to POST, adding automated tests, improving UI styling, and adding pagination or sorting for the products table.

---

## Current Limitations

- Local only — no deployment yet
- UI is functional but unstyled
- `base.html`, `style.css`, and `docs/architecture.md` are stubs
- Sync is triggered manually
- `/sync` uses GET for convenience during local testing — should be POST before any deployment
- No pagination, sorting, or charts yet
- No automated tests
- No authentication

---

## Roadmap

### Next

- Shared Jinja2 base layout
- Frontend styling for dashboard and product table
- Navigation between dashboard and product list
- Pagination and sorting for the products page
- `docs/architecture.md` with data flow notes
- Screenshots after the UI is styled

### Later

- Charts for categories, prices, and stock
- Unit tests for normalization and database helpers
- Docker and deployment config
- Scheduled synchronization
- More advanced filtering
- Authentication if the dashboard becomes more admin-facing
