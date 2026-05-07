DROP TABLE IF EXISTS sync_logs;
DROP TABLE IF EXISTS products;

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

CREATE TABLE sync_logs (
    id SERIAL PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    message TEXT,
    records_imported INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);