# QA Baseline Notes - API Data Integration Dashboard

## Environment

- Local Flask development server
- URL: http://127.0.0.1:5000
- Database: local PostgreSQL
- Browser: Chrome/Edge
- Date: 2026-06-19

## Baseline results

### /db-test - PASS
PostgreSQL connection works locally.

### /sync-preview - PASS
External API fetch and product normalization work. The endpoint returns `products_count: 194` and sample normalized product records.

### /sync - PASS
Products are synchronized successfully. The endpoint returns `success: true` and `records_imported: 194`.

### / - PASS
Dashboard loads successfully and displays:
- total products: 194
- categories: 24
- average price: 1570.1
- low stock products: 25
- latest sync status: success

### /products - PASS
Products page loads successfully and displays product records from the database.

### Search - PASS
Search for `phone` returns filtered product results. The search value remains visible in the input field.

### Category filter - PASS
Filtering by category `smartphones` displays products from the selected category. The selected category remains visible in the dropdown.

### Search + category - PASS
Search for `samsung` within the `smartphones` category returns Samsung smartphone products.

### Repeated sync - PASS
Repeated synchronization does not create duplicate products in the main scenario. The dashboard product count remains 194 after another sync.

## Not checked yet

- empty search results
- invalid category value
- external API failure handling
- database failure handling in UI
- pagination
- sorting
- charts
- automated tests
- deployment