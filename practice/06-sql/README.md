# Hands-On SQL for Data Science

The goal of this activity is to familiarize you with SQL (Structured Query Language) for data science. SQL is essential for querying relational databases, extracting insights from structured data, and managing data stored in database systems.


If the initial examples feel like a breeze, challenge yourself with activities in the *Advanced Concepts* section and explore the resource links at the end of this post.

* Start with the **In-class Exercises**.
* Continue with the **Additional Practices** section on your own time. 
* Optional: Explore the **Advanced Concepts** if you wish to explore SQL in more depth.

## Setup

Before you begin, you'll need to set up your environment to work with MySQL databases. Follow the setup instructions to [configure your Codespace with MySQL support](../../setup/codespace-mysql.md).

## In-class exercises

Complete the Setup steps above before beginning the hands-on exercises below.

### Step 1: Start up a Codespace

Start up a new Codespace from your forked repository using the `MySQL` option. For detailed instructions, see [Start MySQL environment in Codespace](../../setup/codespace-mysql.md#step-2-start-mysql-environment-in-codespace).

### Step 2: Connect to the MySQL instance in AWS RDS

Connect to the remote MySQL database using the command-line client:

```bash
mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u ds2002 -p
```

**Command options explained:**
- `-h`: Specifies the server hosting the database
- `-P`: Specifies the port for communication with the DBMS on the host server (3306 is the default for MySQL)
- `-u`: Username to connect to the DBMS
- `-p`: Triggers a prompt for password (you'll enter it securely after pressing Enter)

When prompted, enter the password from **Canvas > Modules > Week 06 SQL & Relational Databases > AWS_RDS_credentials.txt**.

**Success indicator:** You should see this prompt:
```bash
mysql>
```

This indicates you're connected to the interactive MySQL command line interface and ready to execute SQL commands.

### Step 3: Explore the existing databases and tables. 

```sql
SHOW DATABASES;
```

You should see the `media` database in addition to other databases that are used internally by the MySQL DBMS.

Observe as the new tables are set up:

```sql
USE media;
CREATE TABLE users (
    userid INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25),
    email VARCHAR(50)
);
```

```sql
CREATE TABLE posts (
    postid INT PRIMARY KEY AUTO_INCREMENT,
    message TEXT,
    userid INT
);
```

Let's see what we created. **You can follow along, run these commands:**
```sql
SHOW FULL TABLES;
```

```sql
DESCRIBE users;
```

```sql
DESCRIBE posts;
```

### Step 4: Insert new data

At the moment the tables are empty. Let's change that.

Add yourself to the `users` table.
```sql
USE media;
INSERT INTO users (name, email) VALUES ('YOUR_NAME', 'YOUR_EMAIL@example.com');
```
The `users` table uses the `userid` as the primary key. It is auto-incremented so we don't have to specify its value when inserting new data.

Check the userid auto-assigned to you. Remember it for the next step.
```sql
SELECT * FROM users;
```

Add a post:
```sql
INSERT INTO posts (message, userid) VALUES ('YOUR_MESSAGE_TO_THE_CLASS', YOUR_USER_ID);
```

Like `users`, the `posts` table uses an auto-increment for the primary key `postid` so we don't have to specify its value when inserting new data. But we want to specify userid (you!) to track who posted what. 


After you added your data, search the content of both tables. 

```sql
SELECT * FROM users WHERE LOWER(name) LIKE LOWER('%k%');
```
The `*` is a wildcard, meaning all fields returned by the query will be displayed. The `LIKE` operator can be used in combination with `%` to search string/text/varchar based fields for values that contain the specified search pattern, in this example all records where the `name` field contains a `k` (the casting to `LOWER` makes the search case-insensitive). 

Modify the above search to select records that have a letter from your name.

Let's switch to the `posts` table.

```sql
SELECT * FROM posts;
```

### Step 5: Simple Joins

Let's combine the information in both tables. The relationship between their records is linked through the primary key `userid` in the `users` table and the foreign key `userid` in the `posts` table.

```sql
SELECT users.*, posts.* FROM users LEFT JOIN posts ON users.userid = posts.userid;
```

```sql
SELECT users.*, posts.* FROM users LEFT JOIN posts ON users.userid = posts.userid WHERE posts.postid IS NOT NULL;
```

```sql
SELECT posts.*, users.* FROM posts LEFT JOIN users ON posts.userid = users.userid;
```

You can learn more about joins in this [SQL tutorial](https://www.geeksforgeeks.org/sql/sql-join-set-1-inner-left-right-and-full-joins/).

### Step 6: Creating Views

A view is populated by the results from a stored SQL query, e.g. the results of a filter or join operation. A view is named and shows up in the `SHOW FULL TABLES;` output. 

```sql
CREATE VIEW `msg_by_user` AS SELECT 
    users.*,
    posts.* 
FROM users 
LEFT JOIN posts 
ON users.userid = posts.userid 
WHERE posts.postid IS NOT NULL;
```
In this example the view is named `msg_by_user` and provides the results of posts organized by users.

### Step 7: SQL script files

Instead of typing SQL commands interactively, you can save SQL statements in a file and execute them using input redirection. This is useful for running multiple commands, setting up databases, or executing complex queries.

**From your terminal (outside the MySQL prompt):**

For this example, you should use Codespace in your forked repository. It is set up to run a MySQL server just for you. The host is `dbhost` and you have root access to it. Before you proceed, make sure you followed the setup steps and have a secret `MYSQL_PASSWORD` configured in your Codespace.  

```bash
mysql -h dbhost -u root -p < data.sql
```

This command:
- Connects to the MySQL server (`-h`, `-u`)
- Prompts for your password (`-p`) - the one in your Codespace secret
- Executes all SQL statements in `data.sql` (via input redirection `<`)

**Note:** The `-p` flag (with a space) will prompt for a password. If you want to specify the password directly (not recommended for security), use `-pPASSWORD` (no space between `-p` and the password).

**From within the MySQL prompt:**

If you're already connected to MySQL, you can use the `source` command:

```sql
USE media;
SOURCE data.sql;
```

## SQL queries using Python

There are many Python packages for interacting with SQL databases or databases in general. Below we'll be using the `mysql-connector` package. One of its benefits is that it's easy to install and easy to learn if you are familiar with SQL.

### `env` variables

In your terminal, define the following environment variables:

```bash
DBHOST=ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com
DBUSER=ds2002
DBPASS=<see AWS_RDS_CREDENTIALS.txt on Canvas>
```

### imports

```python
import json
import os
import mysql.connector
```

### read the env variables

```python
# db config stuff
DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "media"
```

### Connection Strings

```python
db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)
```

### Cursor

Create the cursor. You can create one with or without dictionary output.

**Without dictionary (default):**
```python
cursor = db.cursor()
```
- Returns results as **tuples** (ordered sequences)
- Access values by **index position**: `row[0]`, `row[1]`, etc.
- Example: `(1, 'John', 'Doe', 'john@example.com')`
- Access: `row[0]` for id, `row[1]` for first_name, etc.

**With dictionary output:**
```python
cursor = db.cursor(dictionary=True)
```
- Returns results as **dictionaries** (key-value pairs)
- Access values by **column name**: `row['first_name']`, `row['email']`, etc.
- Example: `{'id': 1, 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'}`
- Access: `row['id']`, `row['first_name']`, etc.
- **Benefits**: More readable, self-documenting code; column order doesn't matter

### Query

```python
# Query users table
query = "SELECT * FROM users ORDER BY name LIMIT 20"
cursor.execute(query)
results = cursor.fetchall()
```

### Complete SELECT Example

```python
import json
import os
import mysql.connector

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "media"

db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)
cursor = db.cursor(dictionary=True)

# Query users table
query = "SELECT * FROM users ORDER BY name LIMIT 20"
cursor.execute(query)
results = cursor.fetchall()

for row in results:
    print(f"User ID: {row['userid']}, Name: {row['name']}, Email: {row['email']}")

cursor.close()
db.close()
```

## Insert Data

### Insert into users table

Assume you have data ready to insert as a simple Python list:

```python
name = "Mickey Mouse"
email = "mickey@disney.com"
```

To insert into the users table, use a SQL query with parameterized values:

```python
query = "INSERT INTO users (name, email) VALUES (%s, %s)"
record_data = (name, email)
cursor.execute(query, record_data)
db.commit()
```

### Insert into posts table

To insert a post linked to a user:

```python
message = "Hello, class!"
userid = 1  # The userid from the users table

query = "INSERT INTO posts (message, userid) VALUES (%s, %s)"
record_data = (message, userid)
cursor.execute(query, record_data)
db.commit()
```

### Complete INSERT Example
```python
import json
import os
import mysql.connector

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "media"

db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)
cursor = db.cursor(dictionary=True)

# Insert a new user
name = "Mickey Mouse"
email = "mickey@disney.com"
query = "INSERT INTO users (name, email) VALUES (%s, %s)"
record_data = (name, email)
cursor.execute(query, record_data)
db.commit()

# Get the auto-generated userid
userid = cursor.lastrowid
print(f"Inserted user with ID: {userid}")

# Insert a post for this user
message = "Hello, class! This is my first post."
query = "INSERT INTO posts (message, userid) VALUES (%s, %s)"
record_data = (message, userid)
cursor.execute(query, record_data)
db.commit()

# Close the db connections
cursor.close()
db.close()
```

For production code we'd set up a `if __name__ == "__main__":` block, break up the code into functions, and use a logger instead of print statements.

## Additional Practice

Reference files / commands:

- [`data.sql`](./data.sql)
- [`logistics.sql`](./logistics.sql) | [`logistics_query.py`](./logistics_query.py)
- [`insert_data.py`](./insert_data.py)
- [`select-query.py`](./select-query.py)

### More conditionals

```sql
# Delete a single customer
DELETE FROM customers WHERE customer_key = '12345';
```

```sql
# Delete customer records that are missing a value
DELETE FROM customers WHERE dob IS NULL OR dob = '';
```

```sql
# Delete old customers who have not visited your app recently
DELETE FROM customers WHERE last_visit < '2015-12-31 00:00:00';
```

```sql
# Delete records that meet more complex conditions
DELETE FROM customers 
  WHERE 
    mfa_auth = 0 AND
    last_visit < '2015-12-31 00:00:00' AND
    password_age > 90;
```

### SQL in Jupyter Notebooks

For interactive exploration of the `media` database, use the `ConnectToRds.ipynb` notebook to connect to the database and run queries interactively.

## Advanced Concepts (Optional)

### SQL CLI: Subqueries and Nested Queries

Subqueries allow you to use the result of one query as input for another query. They can be used in SELECT, FROM, WHERE, and HAVING clauses.

```sql
-- Find users who have posted more than the average number of posts
SELECT userid, name, email 
FROM users 
WHERE userid IN (
    SELECT userid 
    FROM posts 
    GROUP BY userid 
    HAVING COUNT(*) > (SELECT AVG(post_count) FROM (SELECT COUNT(*) as post_count FROM posts GROUP BY userid) as subquery)
);
```

### SQL CLI: Aggregate Functions with GROUP BY and HAVING

Use aggregate functions (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`) with `GROUP BY` to summarize data, and `HAVING` to filter grouped results.

```sql
-- Count posts per user and show only users with more than 5 posts
SELECT users.userid, users.name, COUNT(posts.postid) as post_count
FROM users
LEFT JOIN posts ON users.userid = posts.userid
GROUP BY users.userid, users.name
HAVING COUNT(posts.postid) > 5
ORDER BY post_count DESC;
```

### SQL CLI: Indexes for Performance Optimization

Indexes improve query performance by creating a data structure that allows faster lookups. Create indexes on frequently queried columns.

```sql
-- Create an index on the userid column in the posts table
CREATE INDEX idx_userid ON posts(userid);

-- Create a composite index for queries filtering on multiple columns
CREATE INDEX idx_user_post ON posts(userid, postid);

-- View all indexes on a table
SHOW INDEXES FROM posts;
```

### Python: Connection Context Managers and Error Handling

Use context managers (`with` statements) to ensure connections are properly closed, even if errors occur. Implement error handling for robust database operations.

```python
import mysql.connector
from mysql.connector import Error
import os

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "media"

try:
    with mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB) as connection:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM users WHERE userid = %s"
            cursor.execute(query, (1,))
            result = cursor.fetchone()
            print(result)
except Error as e:
    print(f"Error connecting to MySQL: {e}")
```

### Python: Batch Inserts with executemany()

Use `executemany()` to insert multiple rows efficiently in a single operation, which is much faster than executing individual INSERT statements.

```python
import mysql.connector
import os

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "media"

connection = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)
cursor = connection.cursor(dictionary=True)

# Prepare multiple rows of data
users_data = [
    ('Alice Smith', 'alice@example.com'),
    ('Bob Jones', 'bob@example.com'),
    ('Charlie Brown', 'charlie@example.com')
]

# Insert all rows in one operation
query = "INSERT INTO users (name, email) VALUES (%s, %s)"
cursor.executemany(query, users_data)
connection.commit()

print(f"Inserted {cursor.rowcount} rows")
cursor.close()
connection.close()
```

### Python: Connection Pooling for Production Applications

Connection pooling manages a pool of database connections, reusing them efficiently instead of creating new connections for each request. This is essential for production applications.

```python
from mysql.connector import pooling
import os

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "media"

# Configure connection pool
pool_config = {
    'pool_name': 'mypool',
    'pool_size': 5,
    'pool_reset_session': True,
    'host': DBHOST,
    'user': DBUSER,
    'password': DBPASS,
    'database': DB
}

# Create connection pool
connection_pool = pooling.MySQLConnectionPool(**pool_config)

# Get connection from pool
connection = connection_pool.get_connection()

if connection.is_connected():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users LIMIT 10")
    results = cursor.fetchall()
    print(results)
    cursor.close()
    connection.close()  # Returns connection to pool
```

## Resources

[SQL Cheatsheet](https://media.geeksforgeeks.org/wp-content/uploads/20240328180119/SQL-Cheat-Sheet-PDF.pdf)
[SQL Tutorial](https://www.geeksforgeeks.org/sql/sql-tutorial/)
[SQL Commands](https://www.geeksforgeeks.org/sql/sql-ddl-dql-dml-dcl-tcl-commands/)
[SQL Data Types](https://www.geeksforgeeks.org/sql/sql-data-types/)
[SQL Operators](https://www.geeksforgeeks.org/sql/sql-operators/)
[Joins in SQL](https://www.geeksforgeeks.org/sql/sql-join-set-1-inner-left-right-and-full-joins/)
