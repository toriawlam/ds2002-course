use kze4za_db;

select customers.first_name, customers.last_name, orders.order_item, orders.order_date 
from customers join orders on customers.customer_id = orders.customer_id
where orders.order_id is not null;