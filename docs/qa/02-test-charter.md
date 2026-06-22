# Test Charter - API Data Integration Dashboard

## Mission

The goal of this QA pass is to verify the main MVP data integration flow of the API Data Integration Dashboard project.

The focus is on checking whether product data can be fetched from the external API, normalized, synchronized into PostgreSQL, displayed on the dashboard and browsed through the products page with basic search and category filtering.

## Scope

This QA pass covers the following areas:

* PostgreSQL connection check through `/db-test`
* External API preview through `/sync-preview`
* Manual product synchronization through `/sync`
* Product data normalization
* Product saving/updating in PostgreSQL
* Synchronization logging
* Dashboard statistics
* Latest synchronization information on the dashboard
* Products page displaying records from the database
* Product search by title, brand or category
* Category filtering
* Combined search and category filtering
* Repeated synchronization and duplicate prevention in the main tested scenario

## Out of scope

The following areas are not included in this QA pass:

* Performance testing
* Security testing
* Deployment testing
* Cross-browser testing matrix
* Full automated testing
* Playwright tests
* Docker setup
* Scheduled synchronization
* Pagination testing
* Sorting testing
* Charts testing
* Authentication testing

These areas are excluded because they are either not implemented yet, not required for the current local MVP review, or would make this mini QA project too broad.

## Main risks

The main risks for this QA pass are:

* The application depends on the external DummyJSON API.
* The project requires a correctly configured local PostgreSQL database.
* `/sync` uses the GET method while changing database state.
* Error states may not be clearly visible in the UI yet.
* Product list UI is functional but still unstyled.
* There are no automated regression tests yet.
* Repeated manual checks may be needed after changes because the project has no test automation at this stage.

## Test approach

Testing will be performed manually in a local environment.

The main approach includes:

* Opening selected endpoints in the browser
* Checking HTTP responses where applicable
* Verifying dashboard values after synchronization
* Checking whether products are displayed from the database
* Testing search and category filtering behavior
* Repeating synchronization to check whether duplicate products are created
* Using selected PostgreSQL queries later to verify product count and synchronization logs
* Documenting results in manual test cases, execution log and QA observations

## Exit criteria

This QA pass can be considered complete when:

* The main MVP flow is covered by manual test cases
* Test cases have expected results
* Selected tests are executed and documented
* Actual results are recorded in the execution log
* Important observations, limitations or bugs are documented
* The QA documentation clearly separates implemented features from planned or not yet testable areas
* The README contains a short QA review/testing notes section
