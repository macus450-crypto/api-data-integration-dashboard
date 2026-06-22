-- TC-010 - Repeated synchronization duplicate check

SELECT COUNT(*) AS total_products
FROM products;

SELECT COUNT(DISTINCT external_id) AS unique_external_ids
FROM products;