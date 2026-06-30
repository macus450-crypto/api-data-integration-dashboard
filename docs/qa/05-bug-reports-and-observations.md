# Bug Reports and QA Observations - API Data Integration Dashboard

## Purpose

This document summarizes bugs, limitations, risks and QA observations found during the manual QA pass for the API Data Integration Dashboard project.

The goal is to document not only test failures, but also important quality-related findings that may affect maintainability, usability, testability or future development.

## Summary

During this QA pass, the main MVP data integration flow was tested manually.

The following areas were verified:

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

All executed manual test cases passed in the tested local environment.

No critical functional bugs were found in the main MVP flow.

## Bugs found

No critical functional bugs were found during this QA pass.

## Observations and limitations

### OBS-001 - `/sync` state-changing action uses POST

**Type:** Resolved technical observation  
**Severity:** Resolved  
**Priority:** Resolved

**Description:**

The `/sync` action changes application state by fetching products from the external API, saving or updating records in PostgreSQL and creating a synchronization log. This flow is now triggered by a POST form from the dashboard **Run sync** button.

**Why it matters:**

POST is more appropriate for actions that change database state. It reduces the risk of accidental synchronization through direct page visits, browser refreshes, link previews, crawlers or monitoring tools.

**Current status:**

Resolved. `/sync` uses POST, redirects back to the dashboard, and shows the result through a flash message.

---

### OBS-002 - Basic UI styling has been added

**Type:** Resolved UX / UI observation
**Severity:** Resolved
**Priority:** Resolved

**Description:**

The dashboard and products page now use custom CSS for layout, cards, tables, filters, buttons, status badges, empty states and responsive behavior.

**Why it matters:**

A styled interface improves readability, usability and professional presentation for a portfolio project.

**Current status:**

Resolved. Future UI work should focus on feature polish, visual regression checks and refreshed screenshots after larger changes.

---

### OBS-003 - Product list has no pagination

**Type:** Functional limitation  
**Severity:** Low  
**Priority:** Medium

**Description:**

The products page displays many product records in a single table. Pagination is not implemented yet.

**Why it matters:**

For a small dataset the current solution is acceptable, but with larger datasets the page may become harder to use and slower to load.

**Recommendation:**

Add pagination to the products page before expanding the dataset or using the application with larger product collections.

---

### OBS-004 - Product list has no sorting

**Type:** Functional limitation  
**Severity:** Low  
**Priority:** Low

**Description:**

The products table displays records, but users cannot sort them by columns such as price, rating, stock, title or category.

**Why it matters:**

Sorting would make the product list more useful for analysis and browsing.

**Recommendation:**

Add sorting for key product columns in a future iteration.

---

### OBS-005 - Application depends on external DummyJSON API

**Type:** External dependency risk  
**Severity:** Medium  
**Priority:** Medium

**Description:**

The synchronization flow depends on the availability and response structure of the external DummyJSON API.

**Why it matters:**

If the external API is unavailable, slow or changes its response format, synchronization may fail or return unexpected results.

**Recommendation:**

Improve error handling for external API failures and consider adding tests or mocks for API responses.

---

### OBS-006 - Testing is manual only

**Type:** Testability limitation  
**Severity:** Medium  
**Priority:** Medium

**Description:**

The current QA pass was performed manually. There are no automated regression tests yet.

**Why it matters:**

Manual testing is useful for the current MVP review, but future changes may accidentally break existing functionality. Without automated tests, regression testing must be repeated manually.

**Recommendation:**

Add automated tests for core logic such as product normalization, database save/update behavior, search filtering and synchronization flow.

---

### OBS-007 - Local PostgreSQL setup is required

**Type:** Environment dependency  
**Severity:** Low  
**Priority:** Medium

**Description:**

The project requires a correctly configured local PostgreSQL database and `.env` file.

**Why it matters:**

A missing database, incorrect credentials or missing schema can block testing and development.

**Recommendation:**

Document setup steps clearly in the README and consider adding Docker support in the future.

---

## Positive findings

* Main MVP flow works in the tested local environment.
* Product synchronization runs through a dashboard POST flow and shows a flash message result.
* Dashboard displays product statistics and latest synchronization data.
* Products page displays synchronized records from PostgreSQL.
* Keyword search works.
* Category filtering works.
* Combined search and category filtering works.
* Empty search result behavior is handled with a clear `No products found.` message.
* Repeated synchronization does not create duplicate products in the tested scenario.
* Evidence screenshots were collected for executed test cases.

## Final QA conclusion

The API Data Integration Dashboard MVP is functional in the tested local environment.

The main data integration flow works as expected: products can be fetched from the external API, normalized, synchronized into PostgreSQL, displayed on the dashboard and browsed through the products page with search and category filtering.

No critical functional bugs were found during this QA pass.

The most important improvements for the next iteration are adding automated tests, improving the products table with pagination or sorting, and refreshing QA evidence screenshots after the `/sync` POST and flash-message update.

## Test coverage reference

The QA observations in this document are based on the manual test cases executed in `04-test-execution-log.md`.

| Test ID | Area verified                                     | Result |
| ------- | ------------------------------------------------- | ------ |
| TC-001  | Database connection check                         | PASS   |
| TC-002  | External API preview and product normalization    | PASS   |
| TC-003  | Manual product synchronization                    | PASS   |
| TC-004  | Dashboard statistics after synchronization        | PASS   |
| TC-005  | Products page and product table                   | PASS   |
| TC-006  | Product search by keyword                         | PASS   |
| TC-007  | Category filtering                                | PASS   |
| TC-008  | Combined search and category filtering            | PASS   |
| TC-009  | Empty search result behavior                      | PASS   |
| TC-010  | Repeated synchronization and duplicate prevention | PASS   |

All listed test cases passed in the tested local environment. Detailed actual results and evidence are documented in `04-test-execution-log.md`.
