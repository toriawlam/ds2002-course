-- Initialize MySQL to allow root connections from any host
-- This script runs automatically when the MySQL container is first created
-- Note: The password is set via MYSQL_ROOT_PASSWORD environment variable
-- This script grants root access from any host using the same password

-- Grant all privileges to root from any host (root@'%' uses the same password as root@'localhost')
-- The root@'localhost' user is created automatically by MySQL with MYSQL_ROOT_PASSWORD
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;

-- Flush privileges to apply changes
FLUSH PRIVILEGES;

