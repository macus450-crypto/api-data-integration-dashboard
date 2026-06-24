# Architecture

## Project purpose

Product Data Integration Dashboard is a small Flask application built to practice a realistic data integration workflow.

The application fetches product data from an external API, validates and normalizes the response, stores the records in a PostgreSQL database, logs synchronization results, and presents product statistics in a simple web dashboard.

The main goal of the project is not to build a large production system, but to demonstrate practical understanding of API integration, backend logic, SQL, PostgreSQL, synchronization flow, error handling and technical documentation.

---

## Main data flow

The main data flow in the application is:

```text
DummyJSON Products API
→ services/api_client.py
→ fetch_products()
→ data validation
→ data normalization
→ app.py /sync route
→ database/db.py save_product()
→ PostgreSQL products table
→ database/db.py save_sync_log()
→ PostgreSQL sync_logs table
→ Flask dashboard
→ User
```

In simpler terms:

```text
External API provides product data
→ Python fetches and validates the data
→ the application normalizes the product structure
→ PostgreSQL stores or updates product records
→ synchronization logs are saved
→ the dashboard displays statistics and product data
```

---

## File responsibilities

The project is divided into separate files and folders to keep responsibilities clear.

### `app.py`

Contains Flask routes and request/response handling.

Main routes:

* `/` — displays dashboard statistics and last synchronization status.
* `/products` — displays product list with search and category filtering.
* `/sync-preview` — fetches product data from the external API and returns a preview without saving to the database.
* `/sync` — fetches products, saves them to PostgreSQL, and writes a synchronization log.
* `/db-test` — checks database connection.

`app.py` should coordinate the flow, not contain low-level API or SQL logic.

---

### `services/api_client.py`

Contains logic responsible for communication with the external API.

Main responsibility:

* sending the HTTP request,
* checking response status,
* parsing JSON,
* validating response structure,
* normalizing product data,
* returning a structured result to Flask routes.

The main function is:

```python
fetch_products()
```

This function does not return only a raw list. It returns a structured result:

```python
{
    "success": True,
    "products": [...],
    "message": "Products fetched successfully"
}
```

or, in case of an error:

```python
{
    "success": False,
    "products": [],
    "message": "Error message"
}
```

This makes error handling in `app.py` clearer.

---

### `database/db.py`

Contains PostgreSQL-related logic.

Main responsibilities:

* opening database connections,
* testing database connection,
* saving or updating products,
* saving synchronization logs,
* fetching dashboard statistics,
* fetching product list,
* fetching available categories.

Important functions:

```python
get_connection()
test_connection()
save_product()
save_sync_log()
get_dashboard_stats()
get_products()
get_categories()
```

This file should contain SQL and database logic, not Flask routes or external API requests.

---

### `templates/`

Contains HTML templates rendered by Flask.

Main templates:

* `index.html` — dashboard view.
* `products.html` — product list view.
* `base.html` — planned shared layout, currently not used by templates

---

### `docs/`

Contains technical documentation for the project.

This file explains how the application works internally and how data moves through the system.

---

## API integration

The application uses DummyJSON Products API as the external data source.

Endpoint used by the project:

```text
https://dummyjson.com/products?limit=0
```

The request is executed in:

```text
services/api_client.py
```

inside the function:

```python
fetch_products()
```

The API request uses a timeout to prevent the application from waiting indefinitely:

```python
requests.get(url, timeout=10)
```

The response status is checked using:

```python
response.raise_for_status()
```

This means that HTTP errors such as 404 or 500 can be caught and handled instead of silently passing through the application.

---

## Data validation and normalization

Data from an external API should not be trusted blindly.

The application validates the response before saving products to the database.

### Response-level validation

The application expects the API response to contain a `products` field that is a list.

Expected structure:

```python
{
    "products": [
        {...},
        {...}
    ]
}
```

The code checks whether `products` is actually a list:

```python
if not isinstance(products, list):
    return {
        "success": False,
        "products": [],
        "message": "Invalid response format: 'products' is not a list"
    }
```

This protects the application from unexpected API response formats.

---

### Product-level validation

Each item inside the `products` list should be a dictionary.

The application checks this before using `.get()`:

```python
if not isinstance(product, dict):
    continue
```

This prevents errors such as:

```text
AttributeError: 'str' object has no attribute 'get'
```

The application also skips products that do not contain critical fields:

```python
if product.get("id") is None or not product.get("title"):
    continue
```

The critical fields are:

* `id` — required to create `external_id`,
* `title` — required to display a meaningful product name.

Fields such as `brand`, `category`, `rating` or `thumbnail` are useful, but they are not critical for identifying the product.

---

### Data normalization

The external API uses its own field names.

The application normalizes product data into a controlled internal format:

```python
{
    "external_id": product.get("id"),
    "title": product.get("title"),
    "brand": product.get("brand"),
    "category": product.get("category"),
    "price": product.get("price"),
    "discount_percentage": product.get("discountPercentage"),
    "rating": product.get("rating"),
    "stock": product.get("stock"),
    "thumbnail_url": product.get("thumbnail")
}
```

Examples of normalization:

```text
id → external_id
discountPercentage → discount_percentage
thumbnail → thumbnail_url
```

This makes the rest of the application independent from the original API naming style.

---

## Database layer

The project uses PostgreSQL to store product data and synchronization logs.

### `products` table

The `products` table stores normalized product records.

Important fields include:

* `external_id`,
* `title`,
* `brand`,
* `category`,
* `price`,
* `discount_percentage`,
* `rating`,
* `stock`,
* `thumbnail_url`,
* `created_at`,
* `updated_at`.

The `external_id` field comes from the external API and is used as a stable product identifier.

It is marked as unique to prevent duplicate products.

---

### Preventing duplicates

The application uses an upsert strategy:

```sql
ON CONFLICT (external_id)
DO UPDATE SET ...
```

This means:

```text
If the product does not exist → insert it.
If the product already exists → update it.
```

This prevents duplicated records during repeated synchronizations.

---

### `sync_logs` table

The `sync_logs` table stores information about synchronization attempts.

It stores:

* synchronization status,
* message,
* number of imported records,
* creation date.

Example statuses:

```text
success
partial_success
error
```

This allows the dashboard to show the last synchronization result.

---

## Synchronization flow

The `/sync` route is responsible for importing products into the database.

The flow is:

```text
1. User opens /sync.
2. Flask calls fetch_products().
3. fetch_products() returns success status, products and message.
4. If API fetching fails, an error sync log is saved.
5. If no products are returned, an error sync log is saved.
6. If products exist, each product is passed to save_product().
7. The application counts imported and not imported products.
8. A sync log is saved with success or partial_success status.
9. JSON response is returned to the user.
```

Successful response example:

```json
{
  "success": true,
  "status": "success",
  "message": "Products synchronized successfully",
  "records_imported": 194,
  "records_not_imported": 0
}
```

Partial success response example:

```json
{
  "success": true,
  "status": "partial_success",
  "message": "Products synchronized with some errors. Imported: 190, Not Imported: 4",
  "records_imported": 190,
  "records_not_imported": 4
}
```

Error response example:

```json
{
  "success": false,
  "status": "error",
  "message": "Error while fetching products: ...",
  "records_imported": 0
}
```

---

## Error handling

The project includes basic error handling suitable for an MVP.

Handled cases include:

* external API request failure,
* invalid response format,
* `products` field not being a list,
* individual product not being a dictionary,
* missing critical product fields,
* empty product list,
* database save failures during synchronization,
* database connection errors.

The application does not crash immediately when a single product cannot be saved.

Instead, it counts failed saves and can return a `partial_success` status.

This makes the synchronization process more transparent.

---

## Dashboard flow

The dashboard route `/` uses:

```python
get_dashboard_stats()
```

to fetch aggregated information from PostgreSQL.

The dashboard displays:

* total number of products,
* number of categories,
* average product price,
* number of low stock products,
* last synchronization status,
* last synchronization message,
* number of records imported,
* last synchronization date.

This allows the user to quickly understand the current state of imported product data.

---

## Products list flow

The `/products` route displays products stored in the database.

It supports:

* product search,
* category filtering.

The flow is:

```text
User opens /products
→ Flask reads query parameters
→ get_products(search, category) builds SQL conditions
→ PostgreSQL returns matching products
→ products.html displays the result
```

The SQL query uses parameters instead of directly inserting user input into the query string.

This is safer and easier to maintain.

---

## Search and filtering

Search and filtering are handled in:

```python
get_products(search=None, category=None)
```

The function builds optional SQL conditions depending on query parameters.

Example:

```text
/products?search=phone
/products?category=smartphones
/products?search=phone&category=smartphones
```

The function uses:

```python
conditions = []
parameters = []
```

`conditions` stores optional SQL filters.

`parameters` stores values passed safely to the SQL query.

This keeps query construction flexible and avoids directly injecting user input into SQL.

---

## Current limitations

This is an MVP version of the project, so some features are intentionally limited.

Current limitations:

* The application runs locally.
* Synchronization is triggered manually through `/sync`.
* There is no user authentication.
* There is no advanced frontend design.
* There is no pagination for large product lists yet.
* Partial database save errors are counted, but detailed per-product error logs are not stored yet.
* The project does not include automated tests yet.
* The project is not deployed to production.
* PostgreSQL configuration is local and should be handled carefully in a production environment.

These limitations are acceptable for the current project scope because the goal is to demonstrate a clear data integration workflow, not to build a full production e-commerce platform.

---

## Future improvements

Possible future improvements:

* Add pagination to the product list.
* Add sorting by price, rating or stock.
* Store detailed error logs for failed product saves.
* Add automated tests for API client and database functions.
* Improve frontend styling.
* Add charts for product statistics.
* Add environment setup instructions to README.
* Add deployment configuration.
* Add more detailed validation for numeric fields such as price, rating and stock.

---

## Technical summary

The most important technical idea in this project is the full data integration flow:

```text
External API
→ validation
→ normalization
→ database persistence
→ synchronization logs
→ dashboard presentation
```

The project demonstrates practical junior-level backend skills:

* working with external REST API,
* parsing JSON,
* validating uncertain external data,
* normalizing data into an internal structure,
* saving records to PostgreSQL,
* preventing duplicates with `external_id`,
* using SQL queries for statistics and filtering,
* handling basic errors,
* documenting architecture and decisions.
