# Lab 05: SQL for Data Engineering

The goal of this activity is to get you comfortable with SQL (Structured Query Language) for data engineering workflows. You will practice writing SQL scripts, connecting Python applications to databases, and integrating SQL into ETL pipelines. Follow the steps below to build database-driven applications that demonstrate how SQL powers real-world data systems.

Follow the steps below to complete two main tasks. You will develop SQL scripts and Python programs that interact with MySQL databases. Commit your work to your `ds2002-course` repository and submit the URL to your repo for grading.

## Case Study 1: SQL CLI & Scripts

A colleague approaches you, frustrated and in despair. They've been tediously populating a database with new tables, running one command at a time. The database crashed halfway through, and they have to start over from scratch. You offer to show them the power of SQL scripts—writing out all SQL statements in a file and executing them in bulk. If the database crashes again, they can simply rerun the script and be back up and running in minutes.

You're walking your colleague through the following steps:

### Setup

You'll need access to MySQL command-line tools. Choose one of the following options: A, B, or C. 

**Option A (MySQL Codespace):**
Use Codespace with the MySQL environment (see [setup instructions](../../setup/codespace-mysql.md)). 

```bash
mysql -h dbhost -u root -p
```

**Password:** Make sure you have the `MYSQL_PASSWORD` secret configured in your Codespace.

Create a new database called `<computing_id>_db`, e.g., `khs3z_db`. Use this database for Case Study 1. You have full admin privileges.

**Option B (Docker -> AWS RDS MySQL):**
If you cannot spin up the MySQL Codespace environment, you can do the following in the standard course Codespace or local terminal, assuming the Docker container service is installed:
```bash
docker run -it mysql:8.0 mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u <uva_computing_id> -p
```
Replace `<uva_computing_id>` with your UVA computing ID (no `<>`). The `docker run -it mysql:8.0` command launches the Docker container service. It pulls the MySQL container image (version 8.0) from DockerHub, a central software container registry, and launches the `mysql` CLI in an interactive subprocess with the command line arguments you provided.

**Password:** For MySQL access in AWS RDS, the password is the same as your computing ID.  

**Option C (HPC, Apptainer -> AWS RDS MySQL):**

If you are running on [UVA's HPC cluster](../../setup/hpc.md), you can use Apptainer with Docker images to run MySQL commands.

```bash
module load apptainer
apptainer pull ~/mysql-8.0.sif docker://mysql:8.0
apptainer run ~/mysql-8.0.sif mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u <uva_computing_id>
```

**Password:** For MySQL access in AWS RDS, the password is the same as your computing ID.  

The AWS RDS instance has an empty database `<computing_id>_db` set up for you, e.g., `khs3z_db`. Use this database for Case Study 1. You have full admin privileges.

### Step 1: Create Your Database Schema

1. In the fork of your `ds2002-course` repository, create a new folder `mywork/lab5`.

2. Change to the `mywork/lab5` directory and create a new file `initialize.sql`.

3. Write SQL statements in `initialize.sql` that:
   
   a. Create two related tables of your choosing. The tables should demonstrate a **primary key** and **foreign key** relationship. For example:
      - A `customers` table with `customer_id` as the primary key.
      - An `orders` table with `order_id` as the primary key and `customer_id` as a foreign key referencing `customers`.
      This is just an example; be creative!
   
   b. Each table should have at least 3-4 columns with appropriate data types (INT, VARCHAR, TEXT, DATETIME, etc.).
   
   c. Add at least **10 INSERT statements** for each table, ensuring that:
      - Primary key values are unique
      - Foreign key values in the second table reference valid primary keys in the first table
   
   **Hints:** Review the examples in [Practice 06: SQL](../../practice/06-sql/README.md#step-3-explore-the-existing-databases-and-tables) for table creation syntax. See [Step 4: Insert new data](../../practice/06-sql/README.md#step-4-insert-new-data) for INSERT statement examples.

### Step 2: Execute Your SQL Script

Execute your `initialize.sql` script against the MySQL database:

**Option A (MySQL Codespace):**
```bash
mysql -h dbhost -u root -p < initialize.sql
```

When prompted, enter the password from your Codespace secret `MYSQL_PASSWORD`.

**Option B (Docker -> AWS RDS MySQL):**
```bash
docker run -it mysql:8.0 mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u <uva_computing_id> -p < initialize.sql
```
Replace `<uva_computing_id>` with your UVA computing ID (no `<>`). The `docker run -it mysql:8.0` command launches the Docker container service. It pulls the MySQL container image (version 8.0) from DockerHub, a central software container registry, and launches the `mysql` CLI in an interactive subprocess with the command line arguments you provided.

**Password:** For MySQL access in AWS RDS, the password is the same as your computing ID.

**Option C (HPC, Apptainer -> AWS RDS MySQL):**
```bash
module load apptainer
apptainer pull ~/mysql-8.0.sif docker://mysql:8.0
apptainer run ~/mysql-8.0.sif mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u <uva_computing_id> -p < initialize.sql
```
Replace `<uva_computing_id>` with your UVA computing ID (no `<>`). 

**Password:** For MySQL access in AWS RDS, the password is the same as your computing ID.

**Hint:** See [Step 7: SQL script files](../../practice/06-sql/README.md#step-7-sql-script-files) for more details on executing SQL scripts.

### Step 3: Create a Query Script

1. Create a new file `query.sql` that contains a SQL SELECT query.

2. Your query should:
   - Select a subset of records from your tables
   - Use at least one JOIN operation to combine data from both tables
   - Include a WHERE clause to filter the results

3. Execute the query and save the output to a file:
   
   **Option A (MySQL Codespace):**
   ```bash
   mysql -h dbhost -u root -p < query.sql > query_results.txt
   ```
   
   When prompted, enter the password from your Codespace secret `MYSQL_PASSWORD`.

   **Option B (Docker -> AWS RDS MySQL):**
   ```bash
   docker run -it mysql:8.0 mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u <uva_computing_id> -p < query.sql > query_results.txt
   ```

   **Option C (HPC, Apptainer -> AWS RDS MySQL):**
   ```bash
   module load apptainer
   apptainer pull ~/mysql-8.0.sif docker://mysql:8.0
   apptainer run ~/mysql-8.0.sif mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u <uva_computing_id> -p < query.sql > query_results.txt
   ```
   Your password for the AWS RDS instance is the same as your computing ID.

4. Include `initialize.sql`, `query.sql`, and `query_results.txt` in your `mywork/lab5` folder.

**🎉 Success!** You've created and executed SQL scripts! This demonstrates how database schemas are typically initialized and how queries can be automated. Move on to Case Study 2, or submit your work if you're ready!

## Case Study 2: Building a Database-Driven ISS Tracking System

**The Case:** Remember the space enthusiast group from Lab 04? They loved your ETL pipeline so much that they've expanded their operation! Now they have multiple volunteers tracking the ISS from different locations, and they need a proper database system to:
- Store historical ISS location data from multiple reporters
- Track which volunteer collected each data point
- Query and filter data by reporter
- Maintain data integrity with proper relationships between tables

The group has outgrown CSV files—they need a real database! They've set up a MySQL database called `iss` with two tables: `locations` (for ISS position data) and `reporters` (for tracking who collected each data point).

**Your Task:** Build a complete database-driven system that extends your Lab 04 ETL pipeline. You'll modify your Python code to store data in MySQL instead of CSV files and create query functions that retrieve filtered data. This demonstrates how SQL integrates with data engineering workflows—you're not just writing queries, you're building a production-ready data system!

### Setup

For this task, you will need:

1. **Python3**: Should be available in your path. 

    **If you are on the UVA HPC system**, you have to [set up your Python environment](../../setup/hpc.md#python-setup) first. Then run these two commands to load the correct Python version and preinstalled packages.

    ```bash
    module load miniforge
    source activate ds2002
    ```
    Note how the command line prompt now starts with `(ds2002) ...`

1. **Python Libraries**: Install the required packages:
   ```bash
   pip install mysql-connector-python pandas requests
   ```
   
   If you get permission errors, use:
   ```bash
   pip install --user mysql-connector-python pandas requests
   ```

2. **Database Access**: You'll need the MySQL password from **Canvas > Modules > Week 06 SQL & Relational Databases > AWS_RDS_credentials.txt**.

3. **Environment Variables**: Set up your database connection variables in your terminal:
   ```bash
   export DBHOST='ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com'
   export DBUSER='ds2002'
   export DBPASS='<see AWS_RDS_credentials.txt on Canvas>'
   ```

### Step 1: Understand the Database Schema

Before you start coding, explore the `iss` database to understand its structure:

1. Connect to the MySQL database:
   **Option A (AWS RDS MySQL):**
   ```bash
   mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u ds2002 -p
   ```

   **or Option B (Docker -> AWS RDS MySQL):**
   ```bash
   docker run -it mysql:8.0 mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u ds2002 -p
   ```

   **or Option C (HPC, Apptainer -> AWS RDS MySQL):**
   ```bash
   module load apptainer
   apptainer pull ~/mysql-8.0.sif docker://mysql:8.0
   apptainer run ~/mysql-8.0.sif mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u ds2002 -p
   ```

2. When prompted, enter the password from **Canvas > Modules > Week 06 SQL & Relational Databases > AWS_RDS_credentials.txt**.

3. Explore the database:
   ```sql
   USE iss;
   SHOW TABLES;
   DESCRIBE locations;
   DESCRIBE reporters;
   SELECT * FROM locations LIMIT 5;
   SELECT * FROM reporters LIMIT 5;
   ```

4. Take note of:
   - The column names and data types in the `locations` table
   - The column names and data types in the `reporters` table
   - How the tables are related (what foreign key connects them?)

### Step 2: Modify `iss.py` from Lab 04

1. Copy your `iss.py` file from `mywork/lab4` to `mywork/lab5`.

2. Modify `iss.py` to connect to the MySQL database instead of writing to CSV files. The script should:

   a. **Database Connection**: Connect to the MySQL server using:
      - Host: `ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com`
      - User: `ds2002`
      - Database: `iss`
      - Password: From environment variable or Canvas credentials
      
      **Hint:** Use environment variables for credentials. See [SQL queries using Python](../../practice/06-sql/README.md#sql-queries-using-python) for connection examples.
   
   b. **New Function: `register_reporter`**: Create a function that accepts three arguments:
      - `table`: The table name (should be `'reporters'`)
      - `reporter_id`: Your computing ID (e.g., `'mst3k'`)
      - `reporter_name`: Your name
      
      The function should:
      - Query the `reporters` table to check if the `reporter_id` already exists
      - If the `reporter_id` doesn't exist, INSERT a new record with `reporter_id` and `reporter_name`
      - If it already exists, skip the insertion (or update it)
      - Use parameterized queries to prevent SQL injection
      
      **Hint:** Use `SELECT ... WHERE reporter_id = %s` to check existence, then `INSERT INTO ... VALUES (%s, %s)` if needed. See [Insert Data](../../practice/06-sql/README.md#insert-data) for examples. These patterns are referred to as parameterized statements.
   
   c. **Update the `load` function**: Instead of appending to a CSV file, INSERT the latest ISS location into the `locations` table. The function should insert the following fields:
      - `message`: The message from the API response
      - `latitude`: The latitude value
      - `longitude`: The longitude value
      - `timestamp`: Format as `YYYY-MM-DD HH:MM:SS`. The timestamp from the API may need to be converted to match that format.
      - `reporter_id`: Your computing ID (the same one you registered in `register_reporter`)
      
      **Hint:** Extract these values from the JSON data returned by your `extract` function. Use parameterized INSERT statements. Make sure to call `db.commit()` after inserting.
   
   d. **Call `register_reporter`**: In your `main()` function, call `register_reporter` once at the beginning to ensure your reporter ID is registered in the database.
   
   e. **Error Handling**: Add proper try/except blocks around database operations. Close connections properly using `cursor.close()` and `db.close()` in finally blocks.

3. Test your modified script by running it at least 10 times. Each run should insert a new location record into the database.

4. Confirm successful updates of the `iss` database by querying the `locations` and `reporters` tables.

5. **Optional additional challenge:** Write a Python script that executes a query joining the `reporters` and `locations` tables with optional filtering by `reporter_name` or `reporter_id`. 

**🎉 Success!** You've integrated SQL into your ETL pipeline! Your system now stores data in a database and can query it programmatically. This is how production data engineering systems work—databases provide persistence, relationships, and powerful querying capabilities that CSV files can't match.

## Learning Outcomes

With your SQL integration complete, you've successfully demonstrated how databases power data engineering workflows. You've learned how to:

- Write SQL scripts to create database schemas with primary and foreign keys
- Execute SQL scripts from the command line
- Connect Python applications to MySQL databases
- Use parameterized queries to prevent SQL injection
- Implement database operations in Python
- Use JOIN operations to combine related tables
- Filter data using WHERE clauses and pattern matching
- Export query results to CSV files
- Integrate SQL databases into ETL pipelines

These skills are essential for data engineering. SQL databases provide the persistence, relationships, and querying power that make large-scale data systems possible. The patterns you've practiced here—connecting applications to databases, writing parameterized queries, and using JOINs—are used in every production data system.

## Submit your work

You created the following files for this lab. All files should be in the folder `mywork/lab5` within your fork of the course repository:

**From Case Study 1:**
- `initialize.sql` - SQL script to create tables and insert data
- `query.sql` - SQL query script
- `query_results.txt` - Output from your query execution

**From Case Study 2:**
- `iss.py` - Modified ETL pipeline that stores data in MySQL (copied from `mywork/lab4` and modified)

**Optional (from Step 5 additional challenge):**
- `query.py` - Python script that executes a query joining the `reporters` and `locations` tables with optional filtering by `reporter_name` or `reporter_id`

**Submission Steps:**
1. Add all files to git: `git add mywork/lab5/*`
2. Commit your work: `git commit -m "Complete Lab 05: SQL for Data Engineering"`
3. Push to your repository: `git push origin main`
4. Submit the URL of your forked repository's `mywork/lab5` folder in the Canvas assignment. The URL should look like: `https://github.com/YOUR_USERNAME/ds2002-course/tree/main/mywork/lab5`
