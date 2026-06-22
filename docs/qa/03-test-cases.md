# Manual Test Cases - API Data Integration Dashboard

## Purpose

This document contains manual test cases for the main MVP data integration flow of the API Data Integration Dashboard project.

The test cases focus on local manual testing of implemented and testable features: database connection, external API preview, synchronization, dashboard, products page, search, category filtering and repeated synchronization.

---

## TC-001 - Database connection check

**Preconditions:**

* Application is running locally.
* PostgreSQL is installed and running.
* `.env` file contains valid database connection settings.

**Steps:**

1. Open `http://127.0.0.1:5000/db-test` in the browser.
2. Observe the response.

**Expected result:**

* Endpoint returns a successful response.
* Response confirms that the application is connected to PostgreSQL.
* No server error is displayed.

**Actual result:**

* To be filled during test execution.

**Status:**

* Not run

**Notes:**

* This test verifies only the application database connection, not the full database schema or product data.

---

## TC-002 - External API preview returns normalized products

**Preconditions:**

* Application is running locally.
* External DummyJSON API is available.

**Steps:**

1. Open `http://127.0.0.1:5000/sync-preview` in the browser.
2. Check the response body.
3. Verify that `products_count` is returned.
4. Verify that `sample_products` contains normalized product records.

**Expected result:**

* Endpoint returns a successful response.
* Response contains `products_count`.
* Response contains `sample_products`.
* Sample products include normalized fields such as `external_id`, `title`, `brand`, `category`, `price`, `rating`, `stock` and `thumbnail_url`.
* Data is previewed without saving products to the database.

**Actual result:**

* To be filled during test execution.

**Status:**

* Not run

**Notes:**

* This test checks API fetch and normalization preview only. Database saving is covered by a separate synchronization test.

## TC-003 - Manual product synchronization

**Preconditions:**

* Application is running locally.
* External DummyJSON API is available.
* PostgreSQL is installed and running.
* `.env` file contains valid database connection settings.
* Database schema has been created.

**Steps:**

1. Open `http://127.0.0.1:5000/sync` in the browser.
2. Check the JSON response.
3. Verify that the response contains `success`, `message` and `records_imported`.
4. Open `http://127.0.0.1:5000/`.
5. Verify that the dashboard displays latest synchronization information.

**Expected result:**

* Endpoint returns a successful response.
* Response contains `success: true`.
* Response contains a synchronization success message.
* Response contains `records_imported`.
* Products are saved or updated in PostgreSQL.
* Dashboard displays latest synchronization status after running `/sync`.

**Actual result:**

* To be filled during test execution.

**Status:**

* Not run

**Notes:**

* This test verifies the main manual synchronization flow.
* Duplicate prevention after repeated synchronization should be covered by a separate test case.
* `/sync` currently uses the GET method while changing database state. This is acceptable for local MVP testing, but should be reviewed before deployment.

---

## TC-004 - Dashboard displays product statistics after synchronization

**Preconditions:**
* Application is running locally.
* PostgreSQL is installed and running.
* `.env` file contains valid database connection settings.
* Products have been synchronized by running `/sync`.

**Steps:**
1. Open `http://127.0.0.1:5000/` in the browser.
2. Check the dashboard statistics section.
3. Check the latest synchronization section.

**Expected result:**
* Dashboard page loads without a server error.
* Dashboard displays total products count.
* Dashboard displays categories count.
* Dashboard displays average price.
* Dashboard displays low stock products count.
* Dashboard displays latest synchronization status.
* Latest synchronization section contains status, message, records imported and date.

**Actual result:**
* To be filled during test execution.

**Status:**
* Not run

**Notes:**
* This test verifies whether synchronized database data is visible on the dashboard.
* This test does not validate visual styling because the UI is still basic and styling is planned.

## TC-005 - Products page displays product records

**Preconditions:**

* Application is running locally.
* PostgreSQL is installed and running.
* `.env` file contains valid database connection settings.
* Products have been synchronized by running `/sync`.

**Steps:**

1. Open `http://127.0.0.1:5000/products` in the browser.
2. Check whether the products page loads successfully.
3. Check whether the product table is visible.
4. Verify that product records are displayed in the table.
5. Check whether key columns are visible, such as title, brand, category, price, discount, rating and stock.

**Expected result:**

* Products page loads without a server error.
* Product table is displayed.
* Product records are visible in the table.
* Product details are displayed in the expected columns.
* Search input and category filter are visible on the page.

**Actual result:**

* To be filled during test execution.

**Status:**

* Not run

**Notes:**

* This test verifies whether synchronized product data is visible on the products page.
* This test does not validate every database record against the UI.
* Direct database count or record validation should be covered by a separate SQL/data consistency test.
* This test does not validate visual styling because the UI is still basic and styling is planned.

## TC-006 - Product search by keyword

**Preconditions:**

* Application is running locally.
* PostgreSQL is installed and running.
* `.env` file contains valid database connection settings.
* Products have been synchronized by running `/sync`.

**Steps:**

1. Open `http://127.0.0.1:5000/products` in the browser.
2. Enter `phone` in the search input.
3. Click the `Search` button.
4. Check whether the product list is filtered.
5. Verify that displayed products are related to the search keyword through title, brand or category.
6. Verify that the search input keeps the value `phone`.
7. Verify that a `Clear` link is visible.
8. Click the `Clear` link.
9. Verify that the unfiltered products page is displayed again.

**Expected result:**

* Products page loads without a server error.
* Search input is visible.
* After submitting the search form, the product list is filtered.
* Displayed products are related to the keyword `phone` by title, brand or category.
* Search input keeps the searched value `phone`.
* `Clear` link is visible when search is active.
* After clicking `Clear`, active search is removed and the products page displays the unfiltered product list again.

**Actual result:**

* To be filled during test execution.

**Status:**

* Not run

**Notes:**

* This test verifies keyword search on the products page.
* Search is expected to work across product title, brand and category.
* This test does not validate every database record against the UI.
* This test does not validate visual styling because the UI is still basic and styling is planned.
* This test does not cover combined search and category filtering, which should be covered by a separate test case.

## TC-007 - Category filter displays selected category products

**Preconditions:**

* Application is running locally.
* PostgreSQL is installed and running.
* `.env` file contains valid database connection settings.
* Products have been synchronized by running `/sync`.

**Steps:**

1. Open `http://127.0.0.1:5000/products` in the browser.
2. Select `smartphones` from the category filter.
3. Click the `Search` button.
4. Check whether the product list is filtered.
5. Verify that displayed products belong to the `smartphones` category.
6. Verify that the category dropdown keeps the selected value `smartphones`.
7. Verify that a `Clear` link is visible.
8. Click the `Clear` link.
9. Verify that the unfiltered products page is displayed again.

**Expected result:**

* Products page loads without a server error.
* Category filter is visible.
* After selecting `smartphones` and submitting the form, the product list is filtered.
* Displayed products belong to the `smartphones` category.
* Category dropdown keeps the selected value `smartphones`.
* `Clear` link is visible when category filter is active.
* After clicking `Clear`, active category filter is removed and the products page displays the unfiltered product list again.

**Actual result:**

* To be filled during test execution.

**Status:**

* Not run

**Notes:**

* This test verifies category filtering on the products page.
* This test uses `smartphones` as a known category from the synchronized product data.
* This test does not validate every database record against the UI.
* This test does not validate visual styling because the UI is still basic and styling is planned.
* This test does not cover combined search and category filtering, which should be covered by a separate test case.

## TC-008 - Combined search and category filtering

**Preconditions:**

* Application is running locally.
* PostgreSQL is installed and running.
* `.env` file contains valid database connection settings.
* Products have been synchronized by running `/sync`.

**Steps:**

1. Open `http://127.0.0.1:5000/products` in the browser.
2. Enter `samsung` in the search input.
3. Select `smartphones` from the category filter.
4. Click the `Search` button.
5. Check whether the product list is filtered.
6. Verify that displayed products are related to the search keyword `samsung`.
7. Verify that displayed products belong to the selected category `smartphones`.
8. Verify that the search input keeps the value `samsung`.
9. Verify that the category dropdown keeps the selected value `smartphones`.
10. Verify that a `Clear` link is visible.
11. Click the `Clear` link.
12. Verify that the unfiltered products page is displayed again.

**Expected result:**

* Products page loads without a server error.
* Search input is visible.
* Category filter is visible.
* After submitting the form with both search and category filters, the product list is filtered.
* Displayed products are related to the keyword `samsung`.
* Displayed products belong to the `smartphones` category.
* Search input keeps the searched value `samsung`.
* Category dropdown keeps the selected value `smartphones`.
* `Clear` link is visible when both search and category filters are active.
* After clicking `Clear`, all active filters are removed and the products page displays the unfiltered product list again.

**Actual result:**

* To be filled during test execution.

**Status:**

* Not run

**Notes:**

* This test verifies combined keyword search and category filtering on the products page.
* This test uses `samsung` as a known search term and `smartphones` as a known category from the synchronized product data.
* This test checks whether both filters work together, not only separately.
* This test does not validate every database record against the UI.
* This test does not validate visual styling because the UI is still basic and styling is planned.

## TC-009 - Empty search result behavior

**Preconditions:**

* Application is running locally.
* PostgreSQL is installed and running.
* `.env` file contains valid database connection settings.
* Products have been synchronized by running `/sync`.

**Steps:**

1. Open `http://127.0.0.1:5000/products` in the browser.
2. Enter `xyz-not-existing-123` in the search input.
3. Click the `Search` button.
4. Check whether the products page loads successfully after submitting the search.
5. Verify that no unrelated product records are displayed.
6. Verify whether a clear message indicating no matching products is displayed.
7. Verify that the search input keeps the value `xyz-not-existing-123`.
8. Verify that a `Clear` link is visible.
9. Click the `Clear` link.
10. Verify that the unfiltered products page is displayed again.

**Expected result:**

* Products page loads without a server error.
* Search input is visible.
* After submitting a search term with no matching products, no unrelated product records are displayed.
* A clear empty-state message is displayed, for example: `No products found`.
* Search input keeps the searched value `xyz-not-existing-123`.
* `Clear` link is visible when search is active.
* After clicking `Clear`, active search is removed and the products page displays the unfiltered product list again.

**Actual result:**

* To be filled during test execution.

**Status:**

* Not run

**Notes:**

* This test verifies the behavior of the products page when a search query returns no matching results.
* This test uses `xyz-not-existing-123` as a search term that should not match synchronized product data.
* If no empty-state message is displayed, this should be documented later as a UX observation or failed expectation, depending on the final behavior.
* This test does not validate every database record against the UI.
* This test does not validate visual styling because the UI is still basic and styling is planned.

## TC-010 - Repeated synchronization does not create duplicate products

**Preconditions:**

* Application is running locally.
* External DummyJSON API is available.
* PostgreSQL is installed and running.
* `.env` file contains valid database connection settings.
* Database schema has been created.
* Products have been synchronized at least once by running `/sync`.

**Steps:**

1. Open `http://127.0.0.1:5000/sync` in the browser.
2. Check that the synchronization response is successful.
3. Open `http://127.0.0.1:5000/sync` again.
4. Check that the second synchronization response is successful.
5. Verify the product count on the dashboard.
6. Verify product count and unique `external_id` count directly in PostgreSQL using:

```sql
SELECT COUNT(*) AS total_products FROM products;

SELECT COUNT(DISTINCT external_id) AS unique_external_ids
FROM products;
```

7. Compare the total product count with the number of unique `external_id` values.

**Expected result:**

* Both synchronization attempts return a successful response.
* Dashboard product count remains stable after repeated synchronization.
* Total product count in the database does not increase unexpectedly after repeated synchronization.
* Each product is represented by a unique `external_id`.
* `COUNT(*)` and `COUNT(DISTINCT external_id)` return the same value.
* No duplicate product records are created in the main tested scenario.

**Actual result:**

* To be filled during test execution.

**Status:**

* Not run

**Notes:**

* This test verifies whether repeated synchronization updates existing products instead of creating duplicates.
* The application uses `external_id` as the unique identifier for products from the external API.
* `records_imported` may still be returned after repeated synchronization because the endpoint counts successful save/update operations, not only newly inserted records.
* This test focuses on duplicate prevention and does not validate every product field against the external API.
* This test does not validate visual styling because the UI is still basic and styling is planned.
