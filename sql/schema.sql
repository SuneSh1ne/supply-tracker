-- ==========================================
-- Supply Tracker: структура базы данных
-- ==========================================

-- Поставщики
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Товары
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

-- Поставки (связывает suppliers и products)
CREATE TABLE IF NOT EXISTS deliveries (
    id INTEGER PRIMARY KEY,
    supplier_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    delivery_date TEXT NOT NULL,
    is_paid INTEGER NOT NULL DEFAULT 0,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);