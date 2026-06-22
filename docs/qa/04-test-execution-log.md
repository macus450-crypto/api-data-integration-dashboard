# Test Execution Log - API Data Integration Dashboard

## Purpose

This document contains the execution results for manual QA test cases prepared for the API Data Integration Dashboard project.

The goal is to record what was tested, what the actual result was, whether the test passed, failed or was blocked, and what evidence was collected.

## Environment

* Application: API Data Integration Dashboard
* Environment: local Flask development server
* URL: http://127.0.0.1:5000
* Database: local PostgreSQL
* Browser: Chrome/Edge
* Test date: 2026-06-21

## Status legend

* PASS - actual result matches the expected result.
* FAIL - actual result does not match the expected result.
* BLOCKED - test could not be executed because of an environment or dependency issue.
* NOT RUN - test has not been executed yet.

## Execution summary

| Test ID | Test case                                                   | Status  | Evidence                                                                                                                         |
| ------- | ----------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------- |
| TC-001  | Database connection check                                   | PASS    | `docs/qa/evidence/screenshots/tc-001-db-test.png`                                                                                |
| TC-002  | External API preview returns normalized products            | PASS    | `docs/qa/evidence/screenshots/tc-002-sync-preview.png`                                                                           |
| TC-003  | Manual product synchronization                              | PASS    | `docs/qa/evidence/screenshots/tc-003-sync.png`                                                                                   |
| TC-004  | Dashboard displays product statistics after synchronization | PASS    | `docs/qa/evidence/screenshots/tc-004-dashboard-stats.png`                                                                        |
| TC-005  | Products page displays product records                      | PASS    | `docs/qa/evidence/screenshots/tc-005-products-page.png`                                                                          |
| TC-006  | Product search by keyword                                   | PASS    | `docs/qa/evidence/screenshots/tc-006-search-phone.png`                                                                           |
| TC-007  | Category filter displays selected category products         | PASS    | `docs/qa/evidence/screenshots/tc-007-category-smartphones.png`                                                                   |    
| TC-008  | Combined search and category filtering                      | PASS    | `docs/qa/evidence/screenshots/tc-008-search-samsung-category-smartphones.png`                                                    |               
| TC-009  | Empty search result behavior                                | PASS    | `docs/qa/evidence/screenshots/tc-009-empty-search-result.png`                                                                    |
| TC-010  | Repeated synchronization does not create duplicate products | PASS    | See TC-010 execution details                                                                                                     |



## Execution details

### TC-001 - Database connection check

**Status:** PASS

**Actual result:**

The `/db-test` endpoint returned a successful response and confirmed that the application can connect to the local PostgreSQL database. The response displayed PostgreSQL version information: PostgreSQL 18.3 on 64-bit Windows. No server error was displayed.

**Evidence:**

`docs/qa/evidence/screenshots/tc-001-db-test.png`

---

### TC-002 - External API preview returns normalized products

**Status:** PASS

**Actual result:**

The `/sync-preview` endpoint returned a successful response. The response included `products_count: 194` and `sample_products`.

Sample product records contained normalized fields such as `external_id`, `title`, `brand`, `category`, `price`, `discount_percentage`, `rating`, `stock` and `thumbnail_url`.

This test verified API fetch and product normalization preview only. Database saving was not verified in this test because it is covered by TC-003.

**Evidence:**

`docs/qa/evidence/screenshots/tc-002-sync-preview.png`

---

### TC-003 - Manual product synchronization

**Status:** PASS

**Actual result:**

The `/sync` endpoint returned a successful synchronization response. The response included `success: true`, `message: Products synchronized successfully` and `records_imported: 194`.

After synchronization, the dashboard was opened and latest synchronization information was visible. The dashboard displayed synchronization status `success`, message `Products synchronized successfully`, `records_imported: 194` and synchronization date.

This confirms that the manual synchronization flow can fetch product data, normalize it, save or update it in PostgreSQL and display latest synchronization information on the dashboard.

**Evidence:**

`docs/qa/evidence/screenshots/tc-003-sync.png`

---

### TC-004 - Dashboard displays product statistics after synchronization

**Status:** PASS

**Actual result:**

The dashboard page loaded without a server error. The dashboard displayed product statistics: total products `194`, categories `24`, average price `1570.1` and low stock products `25`.

The latest synchronization section was also visible and displayed status `success`, message `Products synchronized successfully`, records imported `194` and synchronization date.

**Evidence:**

`docs/qa/evidence/screenshots/tc-004-dashboard-stats.png`

---

### TC-005 - Products page displays product records

**Status:** PASS

**Actual result:**

The `/products` page loaded without a server error. The product table was visible and displayed product records from the local PostgreSQL database.

The page displayed key product columns such as title, brand, category, price, discount percentage, rating and stock. Search input and category filter were also visible.

**Evidence:**

`docs/qa/evidence/screenshots/tc-005-products-page.png`

---

### TC-006 - Product search by keyword

**Status:** PASS

**Actual result:**

After entering `phone` in the search input and submitting the form, the `/products` page displayed filtered product results related to the searched keyword. The search input kept the value `phone`, and the `Clear` link was visible.

After clicking `Clear`, the active search filter was removed and the unfiltered products page was displayed again.

**Evidence:**

`docs/qa/evidence/screenshots/tc-006-search-phone.png`

---

### TC-007 - Category filter displays selected category products

**Status:** PASS

**Actual result:**

After selecting `smartphones` in the category filter and submitting the form, the `/products` page displayed filtered product results from the selected category. The category dropdown kept the selected value `smartphones`, and the `Clear` link was visible.

After clicking `Clear`, the active category filter was removed and the unfiltered products page was displayed again.

**Evidence:**

`docs/qa/evidence/screenshots/tc-007-category-smartphones.png`

---

### TC-008 - Combined search and category filtering

**Status:** PASS

**Actual result:**

After entering `samsung` in the search input, selecting `smartphones` in the category filter and submitting the form, the `/products` page displayed filtered product results matching both conditions. Displayed products were related to the keyword `samsung` and belonged to the `smartphones` category.

The search input kept the value `samsung`, the category dropdown kept the selected value `smartphones`, and the `Clear` link was visible.

After clicking `Clear`, both active filters were removed and the unfiltered products page was displayed again.

**Evidence:**

`docs/qa/evidence/screenshots/tc-008-search-samsung-category-smartphones.png`

---

### TC-009 - Empty search result behavior

**Status:** PASS

**Actual result:**

After entering `xyz-not-existing-123` in the search input and submitting the form, the `/products` page loaded without a server error. No unrelated product records were displayed.

The page displayed a clear empty-state message: `No products found.` The search input kept the value `xyz-not-existing-123`, and the `Clear` link was visible.

After clicking `Clear`, the active search filter was removed and the unfiltered products page was displayed again.

**Evidence:**

`docs/qa/evidence/screenshots/tc-009-empty-search-result.png`

---

### TC-010 - Repeated synchronization does not create duplicate products

**Status:** PASS

**Actual result:**

The `/sync` endpoint was executed repeatedly and returned a successful synchronization response. The response confirmed that products were synchronized successfully.

After repeated synchronization, the dashboard product count remained stable at `194`.

PostgreSQL verification confirmed that the total number of product records and the number of unique `external_id` values were equal:

* total products: `194`
* unique external IDs: `194`

This confirms that repeated synchronization updates existing product records instead of creating duplicate products in the main tested scenario.

**Evidence:**

`docs/qa/evidence/screenshots/tc-010-repeated-sync.png`

`docs/qa/evidence/screenshots/tc-010-sql-product-count.png`

`docs/qa/evidence/db-queries/tc-010-product-count.sql`

