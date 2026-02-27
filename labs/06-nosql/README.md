# Lab 06: NoSQL with MongoDB

The goal of this lab is to get you comfortable with NoSQL document databases using MongoDB. You will use the `mongosh` shell to create collections, insert and query documents, and then use PyMongo to build a small Python application that talks to MongoDB Atlas. Follow the steps below to complete two case studies that show how flexible, schema-free data stores power modern applications.

Commit your work to your `ds2002-course` repository and submit the URL to your repo for grading.

## Setup

Before you begin, set up MongoDB Atlas and connect from your environment. Follow the [MongoDB Atlas setup instructions](../../practice/07-nosql/README.md#set-up-your-own-mongodb-atlas-cluster-in-the-cloud) in Practice 07 (NoSQL): sign up for Atlas, add the required IP access list entries, get your connection string, and save `MONGODB_ATLAS_URL`, `MONGODB_ATLAS_USER`, and `MONGODB_ATLAS_PWD` in your `~/.bashrc` (or equivalent). 

I recommend doing this exercise on UVA's HPC system. Load `mongosh` as described in the [mongosh CLI section](../../practice/07-nosql/README.md#the-mongosh-cli-tool) so you can run the first case study.

---

## Case Study 1: The Bookstore’s New Inventory System (mongosh)

A local bookstore owner has been struggling to track authors and books on spreadsheets. They’ve heard that document databases are great for semi-structured data and want to try MongoDB. They’ve recruited you to design a small “authors” collection and show them how to query it from the shell. No rigid tables—just documents that can grow over time.

You’ll use `mongosh` to create a database, add author documents with nested “bio” fields, run updates, and capture your commands in a script they can reuse.

### Step 1: Create the database and collection

1. Connect to MongoDB Atlas using `mongosh` and your Atlas credentials (see [Connect](../../practice/07-nosql/README.md#3-connect) in Practice 07).

2. Create a new database named `bookstore`. In MongoDB, you switch to (or create) a database with `use <dbname>`; the collection is created when you first insert into it.

3. Insert the following document into the `authors` collection. The `authors` collection will be created automatically when the first document is inserted. Note the nested `bio` object with `short` and `long` fields—this is the kind of flexible structure document databases handle well.

   ```javascript
   db.authors.insertOne({
     "name": "Jane Austen",
     "nationality": "British",
     "bio": {
       "short": "English novelist known for novels about the British landed gentry.",
       "long": "Jane Austen was an English novelist whose works critique and comment upon the British landed gentry at the end of the 18th century. Her most famous novels include Pride and Prejudice, Sense and Sensibility, and Emma, celebrated for their wit, social commentary, and masterful character development."
     }
   })
   ```

4. Update that document to add a `birthday` field with an appropriate value (e.g. `"1775-12-16"` or a date type). Use `updateOne` with a filter and `$set`.

5. Add four more author documents of your choice, using the same structure: `name`, `nationality`, `bio` (with nested `short` and `long`), and `birthday`. Vary nationalities so you can practice filtering. You can do this sequentially with `insertOne` or in bulk with `insertMany`.

6. Run a query that returns the total number of documents in `authors` (e.g. `countDocuments`).

7. Run a query that returns all documents where `nationality` is `"British"`, sorted by `name` in ascending order. (Check your spelling—e.g. `"British"` not `"Bristish"`—so the filter matches.)

8. In the `mongosh` shell, run `history()` to view your recent commands. Copy the commands that correspond to steps 2–7 above (use database, insert first author, update, insert four more, count, British + sort) into a single file so the bookstore owner can rerun them.

   Create a file named `bookstore.js` in `mywork/lab6` with this structure:

   ```javascript
   // Task 2: use database
   // <paste your use bookstore>

   // Task 3: insert first author
   // <paste your insertOne>

   // Task 4: update to add birthday
   // <paste your updateOne>

   // Task 5: insert four more authors
   // <paste your insertMany or insertOne x4>

   // Task 6: total count
   // <paste your countDocuments>

   // Task 7: British authors, sorted by name
   // <paste your find + sort>
   ```

   Use comments so each section is clearly labeled. The owner doesn’t need to run `history()` themselves—they can run the pasted commands in order from `bookstore.js`.

**Success:** You’ve designed a small document model and used the MongoDB shell to create, update, query, and sort documents. Next, you’ll do the same kind of work from Python.

---

## Case Study 2: Bookstore Inventory from Python (PyMongo)

The bookstore owner is impressed by the shell demo. Now they want a simple Python script that connects to the same Atlas cluster, reads from the `bookstore` database, and prints a short report (e.g. how many authors, and a list of names and nationalities). This way they can eventually hook scripts into their workflow or a small dashboard.

**Your task:** Write a Python script that uses PyMongo to connect to MongoDB Atlas, targets the `bookstore` database and `authors` collection from Case Study 1, and produces a small, readable report.

### Step 1: Environment and dependencies

1. Ensure your Atlas environment variables are set in the shell you’ll use (e.g. `MONGODB_ATLAS_URL`, `MONGODB_ATLAS_USER`, `MONGODB_ATLAS_PWD`). If you use a virtual environment or HPC, activate it first (e.g. `module load miniforge && source activate ds2002` on HPC).

2. Install PyMongo if needed:

   ```bash
   pip install pymongo
   ```

   (Use `pip install --user pymongo` if you get permission errors.)

### Step 2: Write the script

3. In `mywork/lab6`, create a script (e.g. `bookstore_report.py`) that:

   - The script should have an `if __name__ == "__main__":` block that calls a `main()` function.
   - Uses `os.getenv()` to read `MONGODB_ATLAS_URL`, `MONGODB_ATLAS_USER`, and `MONGODB_ATLAS_PWD` (e.g. outside of the `main` function).
   - The main function should:
     - Connect to MongoDB Atlas using `pymongo.MongoClient` with the connection string and credentials (see [Practice 07 – MongoDB + Python](../../practice/07-nosql/README.md#mongodb--python) and the `database.py` pattern).
     - Select the `bookstore` database and the `authors` collection.
     - Print a short report that includes:
       - The total number of author documents.
       - For each author, at least the `name` and `nationality` (and optionally `birthday` or `bio.short`). Format the output so it’s easy to read (e.g. one line per author or a few lines per author).
     - Close the client connection.
   - **Optional:** Convert the print statements to logging statements. See earlier labs.

4. Run the script and confirm it connects to Atlas and prints the report from the documents you added in Case Study 1.

**Hint:** Use `collection.count_documents({})` for the total count and `collection.find({})` (with an optional projection) to iterate over authors.

**Success:** You’ve connected to the same MongoDB data from Python and produced a simple report. That’s the same pattern used in larger systems: shell for ad hoc operations, Python (or another driver) for automation and applications.

---

## Learning Outcomes

By completing this lab, you have:

- Used the MongoDB shell (`mongosh`) to create a database and collection and to insert, update, and query documents.
- Practiced filtering and sorting documents and capturing shell commands in a script file.
- Connected to MongoDB Atlas from Python with PyMongo and environment variables.
- Written a small script that reads from a document collection and produces a report.

These skills translate directly to real-world use: document stores like MongoDB are common in data pipelines, APIs, and applications where schema flexibility and nested data are useful.

---

## Submit your work

All deliverables should be in the folder `mywork/lab6` in your fork of the course repository.

**From Case Study 1:**

- `bookstore.js` – Commented script of the mongosh commands you used (steps 2–7), in order, so the bookstore owner can rerun them.

**From Case Study 2:**

- `bookstore_report.py` (or the name you chose) – Python script that connects to Atlas, reads from `bookstore.authors`, and prints the report (count + author list with name and nationality at minimum).

**Submission steps:**

1. Add your files: `git add mywork/lab6/*`
2. Commit: `git commit -m "Complete Lab 06: NoSQL with MongoDB"`
3. Push: `git push origin main`
4. Submit the URL of your `mywork/lab6` folder in the Canvas assignment, e.g.  
   `https://github.com/YOUR_USERNAME/ds2002-course/tree/main/mywork/lab6`
