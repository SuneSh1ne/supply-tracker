-- ==========================================
-- Supply Tracker: SQL-запросы
-- ==========================================

-- ==========================================
-- ЗАПРОС 1. Список всех поставщиков (SELECT)
-- ==========================================
SELECT id, name
FROM suppliers
ORDER BY name;

-- ==========================================
-- ЗАПРОС 2. Список товаров дороже 20 руб. (WHERE)
-- ==========================================
SELECT id, name, price
FROM products
WHERE price >= 20.0
ORDER BY price DESC;

-- ==========================================
-- ЗАПРОС 3. Список активных поставок (WHERE)
-- ==========================================
SELECT id, supplier_id, product_id, quantity, delivery_date
FROM deliveries
WHERE is_cancelled = 0
ORDER BY delivery_date;

-- ==========================================
-- ЗАПРОС 4. Список отменённых поставок (WHERE)
-- ==========================================
SELECT id, supplier_id, product_id, quantity, delivery_date
FROM deliveries
WHERE is_cancelled = 1
ORDER BY delivery_date;

-- ==========================================
-- ЗАПРОС 5. Полная информация о поставках (JOIN)
-- ==========================================
SELECT
    deliveries.id,
    deliveries.delivery_date,
    deliveries.quantity,
    deliveries.is_paid,
    deliveries.is_cancelled,
    suppliers.name AS supplier_name,
    products.name AS product_name,
    products.price AS product_price
FROM deliveries
JOIN suppliers ON deliveries.supplier_id = suppliers.id
JOIN products ON deliveries.product_id = products.id
ORDER BY deliveries.delivery_date;

-- ==========================================
-- ЗАПРОС 6. Поставки конкретного поставщика (JOIN + WHERE)
-- ==========================================
SELECT
    deliveries.id,
    deliveries.delivery_date,
    deliveries.quantity,
    products.name AS product_name,
    products.price AS product_price
FROM deliveries
JOIN products ON deliveries.product_id = products.id
WHERE deliveries.supplier_id = 1
  AND deliveries.is_cancelled = 0
ORDER BY deliveries.delivery_date;

-- ==========================================
-- ЗАПРОС 7. Количество поставок по статусам (GROUP BY)
-- ==========================================
SELECT
    is_cancelled,
    COUNT(*) AS count
FROM deliveries
GROUP BY is_cancelled;

-- ==========================================
-- ЗАПРОС 8. Количество поставок по поставщикам (JOIN + GROUP BY)
-- ==========================================
SELECT
    suppliers.name AS supplier_name,
    COUNT(deliveries.id) AS deliveries_count
FROM suppliers
LEFT JOIN deliveries
    ON suppliers.id = deliveries.supplier_id
    AND deliveries.is_cancelled = 0
GROUP BY suppliers.id, suppliers.name
ORDER BY deliveries_count DESC;

-- ==========================================
-- ЗАПРОС 9. Общая стоимость по поставщикам (SUM + JOIN + GROUP BY)
-- ==========================================
SELECT
    suppliers.name AS supplier_name,
    SUM(deliveries.quantity * products.price) AS total_cost
FROM deliveries
JOIN suppliers ON deliveries.supplier_id = suppliers.id
JOIN products ON deliveries.product_id = products.id
WHERE deliveries.is_cancelled = 0
GROUP BY suppliers.id, suppliers.name
ORDER BY total_cost DESC;

-- ==========================================
-- ЗАПРОС 10. Поставщики с >1 активной поставкой (HAVING)
-- ==========================================
SELECT
    suppliers.name AS supplier_name,
    COUNT(deliveries.id) AS deliveries_count
FROM suppliers
JOIN deliveries ON suppliers.id = deliveries.supplier_id
WHERE deliveries.is_cancelled = 0
GROUP BY suppliers.id, suppliers.name
HAVING COUNT(deliveries.id) > 1
ORDER BY deliveries_count DESC;

-- ==========================================
-- ЗАПРОС 11. Поставки, НЕ принятые на заданную дату (NOT IN + параметр)
-- Параметр ? = '15.09.2026'
-- ==========================================
SELECT
    deliveries.id,
    deliveries.delivery_date,
    suppliers.name AS supplier_name,
    products.name AS product_name
FROM deliveries
JOIN suppliers ON deliveries.supplier_id = suppliers.id
JOIN products ON deliveries.product_id = products.id
WHERE deliveries.id NOT IN (
    SELECT d.id
    FROM deliveries d
    WHERE d.delivery_date = ?
      AND d.is_cancelled = 0
)
  AND deliveries.is_cancelled = 0
ORDER BY deliveries.delivery_date;

-- ==========================================
-- ЗАПРОС 12. Топ-3 самых дорогих товаров (LIMIT + ORDER BY)
-- ==========================================
SELECT id, name, price
FROM products
ORDER BY price DESC
LIMIT 3;

-- ==========================================
-- ЗАПРОС 13. Товары, по которым не было активных поставок (LEFT JOIN)
-- ==========================================
SELECT
    products.id,
    products.name,
    products.price
FROM products
LEFT JOIN deliveries
    ON products.id = deliveries.product_id
    AND deliveries.is_cancelled = 0
WHERE deliveries.id IS NULL
ORDER BY products.name;