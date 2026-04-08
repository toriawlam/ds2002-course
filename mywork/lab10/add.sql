use kze4za_db;

INSERT INTO customers (first_name, last_name, phone)
VALUES ('Emma', 'Stone', 7035551111);

INSERT INTO customers (first_name, last_name, phone)
VALUES ('Ryan', 'Gosling', 7035552222);

INSERT INTO orders (customer_id, order_item, order_date)
VALUES (11, 'Fries', '2026-04-08 12:15:00');

INSERT INTO orders (customer_id, order_item, order_date)
VALUES (12, 'Pizza', '2026-04-08 12:30:00');

INSERT INTO orders (customer_id, order_item, order_date)
VALUES (11, 'Tea', '2026-04-08 12:45:00');
