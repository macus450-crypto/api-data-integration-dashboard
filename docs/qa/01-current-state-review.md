# Current State Review - API Data Integration Dashboard

## Purpose

This document describes the current testable state of the API Data Integration Dashboard project. The goal is to separate implemented features from partially ready, planned, or not yet testable areas.

## Implemented

* `/db-test` endpoint for checking the local PostgreSQL connection
* `/sync-preview` endpoint for fetching and previewing normalized product data without saving it to the database
* `/sync` endpoint for manually synchronizing products from the external API into PostgreSQL
* Product normalization from the external API response
* Product saving/updating in PostgreSQL using `external_id`
* Synchronization logging with status, message, imported records count and timestamp
* Dashboard page with product statistics and latest synchronization information
* `/products` page displaying product records from the database
* Product search by title, brand or category
* Category filter populated from database categories
* Combined search and category filtering
* Repeated synchronization without creating duplicate products in the main tested scenario

## Partially ready

* Dashboard UI is functional but visually unstyled.
* Product list UI is functional but still basic and unstyled.
* Search and category filtering work, but empty-result behavior still needs to be checked.
* Product list displays matching records, but pagination and sorting are not implemented yet.

## Planned / not ready for testing

* Frontend styling
* Pagination for the product list
* Sorting for the product list
* Charts for dashboard data
* Automated tests
* Deployment configuration
* Docker support
* Scheduled synchronization

## Testability risks

* The application depends on the external DummyJSON API, so synchronization results may be affected if the API is unavailable or changes its response structure.
* The project requires a correctly configured local PostgreSQL database.
* `/sync` uses the GET method while changing database state. This is acceptable for local MVP testing, but should be changed to POST before deployment.
* Some error states may not be clearly visible in the UI yet.
* There are no automated tests yet, so regression testing currently depends on manual checks.

## Notes for next QA pass

* Check empty search results, for example `xyz-not-existing`.
* Check invalid or non-existing category values.
* Check whether the UI clearly communicates no results or error states.
* Verify product count directly in PostgreSQL after repeated synchronization.
* Verify recent records in `sync_logs`.
* Prepare manual test cases for the implemented MVP features.
