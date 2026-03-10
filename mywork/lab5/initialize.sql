use kze4za_db;

create table customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone BIGINT
);
create table orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_item VARCHAR(50),
    order_date DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
insert into customers (first_name, last_name, phone) values ('Victoria', 'Lam', 7031234567);
insert into customers (first_name, last_name, phone) values ('Andrew', 'Garfield', 7032468101);
insert into customers (first_name, last_name, phone) values ('Tom', 'Holland', 7032987654);
insert into customers (first_name, last_name, phone) values ('Zendaya', 'Coleman', 7031234567);
insert into customers (first_name, last_name, phone) values ('Zooey', 'Deschanel', 5718302021);
insert into customers (first_name, last_name, phone) values ('Jennifer', 'Lopez', 3822914758);
insert into customers (first_name, last_name, phone) values ('Ted', 'Lasso', 7289103283);
insert into customers (first_name, last_name, phone) values ('Kali', 'Uchis', 8291028392);
insert into customers (first_name, last_name, phone) values ('Don', 'Toliver', 8723946782);
insert into customers (first_name, last_name, phone) values ('Baby', 'Keem', 8736491032);

insert into orders (customer_id, order_item, order_date) values (1, 'Sandwich', '2026-03-09 11:30:15');
insert into orders (customer_id, order_item, order_date) values (2, 'Cookie', '2026-03-09 17:42:17');
insert into orders (customer_id, order_item, order_date) values (3, 'Salad', '2026-03-09 12:00:25');
insert into orders (customer_id, order_item, order_date) values (4, 'Burger', '2026-03-09 18:10:10');
insert into orders (customer_id, order_item, order_date) values (5, 'Sandwich', '2026-03-09 18:32:17');
insert into orders (customer_id, order_item, order_date) values (6, 'Shake', '2026-03-09 18:41:16');
insert into orders (customer_id, order_item, order_date) values (7, 'Smoothie', '2026-03-09 19:00:05');
insert into orders (customer_id, order_item, order_date) values (8, 'Cookie', '2026-03-09 19:02:14');
insert into orders (customer_id, order_item, order_date) values (9, 'Salad', '2026-03-09 19:10:26');
insert into orders (customer_id, order_item, order_date) values (10, 'Soda', '2026-03-09 19:12:35');