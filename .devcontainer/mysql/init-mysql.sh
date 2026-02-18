#!/bin/bash
# Initialize MySQL to allow root connections from any host
# This script runs automatically when the MySQL container is first created
# The MySQL entrypoint executes this script after MySQL is initialized

# Get the root password from environment variable (set by docker-compose)
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD}"

# Create root user for remote connections and grant privileges
# Note: root@'localhost' already exists with MYSQL_ROOT_PASSWORD
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<EOF
CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY '$MYSQL_ROOT_PASSWORD';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

