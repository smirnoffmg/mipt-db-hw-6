DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS customer CASCADE;

CREATE TABLE customer (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(10),
    dob DATE,
    job_title VARCHAR(200),
    job_industry_category VARCHAR(100),
    wealth_segment VARCHAR(50),
    deceased_indicator VARCHAR(1),
    owns_car VARCHAR(10),
    address TEXT,
    postcode INTEGER,
    state VARCHAR(50),
    country VARCHAR(100),
    property_valuation INTEGER
);

CREATE TABLE product (
    product_id INTEGER NOT NULL,
    brand VARCHAR(100),
    product_line VARCHAR(100),
    product_class VARCHAR(50),
    product_size VARCHAR(50),
    list_price NUMERIC(10,2) NOT NULL,
    standard_cost NUMERIC(10,2)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    online_order BOOLEAN,
    order_status VARCHAR(50) NOT NULL
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity NUMERIC(10,2) NOT NULL,
    item_list_price_at_sale NUMERIC(10,2) NOT NULL,
    item_standard_cost_at_sale NUMERIC(10,2)
);

