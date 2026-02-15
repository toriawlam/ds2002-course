# Working with file formats and cleaning data

The goal of this activity is to familiarize you with working with various file formats (JSON, CSV, TSV, XML, SQL) and cleaning data. These skills are essential for processing real-world data, handling different data structures, and preparing data for analysis. They also lay the foundation for working with databases.

> **Note:** Work through the examples below in your terminal (Codespace or local), experimenting with each command and its various options. If you encounter an error message, don't be discouraged—errors are learning opportunities. Reach out to your peers or instructor for help when needed, and help each other when you can. 

* Start with the **In-class Exercises**.
* Continue with the **Additional Practices** section on your own time. 
* Optional: Explore the **Advanced Concepts** if you wish to explore file formats and data cleaning in more depth.

## In-class Exercises

Let's dive into a real-world case study. Start with [Lab 04: Data Formats - ETL Pipeline Basics](../../labs/04-dataformats/README.md)

## Additional Practice

### Working with csv and tsv files

CSV (Comma-Separated Values) files use commas to separate columns:
```csv
name,age,city
Alice,25,New York
Bob,30,San Francisco
Charlie,35,Chicago
```

TSV (Tab-Separated Values) files use tabs to separate columns:
```tsv
name	age	city
Alice	25	New York
Bob	30	San Francisco
Charlie	35	Chicago
```

#### Exercise: Downloading and Processing CSV Data

In this exercise, we'll download the 2018 Central Park Squirrel Census data and perform various operations using Linux CLI commands.

**Step 1: Download the CSV file**

Download the squirrel census data and save it as `squirrel-census.csv`:
```bash
curl -o squirrel-census.csv https://data.cityofnewyork.us/api/views/ej9h-v6g2/rows.csv
```

**Explanation:** The `curl` command fetches the file from the URL. The `-o` flag specifies the output filename.

**Step 2: View the column headers**

Display the first line (header row) of the CSV file:
```bash
head -n 1 squirrel-census.csv
```

**Step 3: Count the number of rows**

Count the total number of rows in the file:
```bash
wc -l squirrel-census.csv
```

The `wc -l` command counts the number of lines in the file. Note: This includes the header row, so subtract 1 for the actual data row count.

**Step 4: Count the number of columns**

Count the number of columns by counting commas in the header row:
```bash
head -n 1 squirrel-census.csv | tr ',' '\n' | wc -l
```

Approach:
- We're using the `|` to connect multiple commands into a pipeline 
- `head -n 1` gets the header row
- `tr ',' '\n'` replaces commas with newlines, creating one line per initial column
- `wc -l` counts the resulting lines (columns)

**Step 5: Filter rows by index and save to a new file**

Extract rows 1-100 (including header) and save to a new file:
```bash
head -n 101 squirrel-census.csv > squirrel-census-sample.csv
```

The `head -n 101` command gets the first 101 lines (1 header + 100 data rows), and `>` redirects the output to a new file.

**Step 6: Extract specific rows by index**

Extract rows 50-100 (excluding header) and save to a new file:
```bash
sed -n '51,101p' squirrel-census.csv > squirrel-census-rows50-100.csv
```

The `sed -n '51,101p'` command prints lines 51 through 101 (0-indexed would be rows 50-100). We start at line 51 because line 1 is the header.

**Step 7: Extract the first three columns using cut**

Extract the first three columns from the original file:
```bash
cut -d',' -f1,2,3 squirrel-census.csv > squirrel-census-first3cols.csv
```

Approach:
- `cut` extracts specific columns from a file
- `-d','` sets the delimiter to comma
- `-f1,2,3` selects the first, second, and third columns
- The output is redirected to a new file

**Step 8: Filter rows based on content and extract columns**

Filter rows containing a specific value in the first column, then extract the first three columns:
```bash
grep "AM" squirrel-census.csv | cut -d',' -f1,2,3 > squirrel-census-filtered.csv
```

Approach:
- `grep "AM"` filters lines containing "AM" (e.g., morning observations)
- `cut -d',' -f1,2,3` extracts the first three columns
- The filtered and extracted data is saved to a new file

**Step 9: Combine filtering and column extraction**

Extract rows 1-50 and get only the first three columns:
```bash
head -n 51 squirrel-census.csv | cut -d',' -f1,2,3 > squirrel-census-sample-first3cols.csv
```

This combines `head` to limit rows and `cut` to limit columns, creating a smaller subset of the data.

#### Convert CSV to TSV

Now let's convert the squirrel census CSV file to TSV format. We'll use the `squirrel-census.csv` file we downloaded earlier and convert it to tab-separated format.

**Method 1: Using `tr`**

Replace commas with tabs:
```bash
tr ',' '\t' < squirrel-census.csv > squirrel-census.tsv
```

The `tr` command translates characters. `','` is replaced with `'\t'` (tab character). The `<` redirects input from the CSV file, and `>` redirects output to the TSV file.

**Method 2: Using `sed`**

Replace commas with tabs using sed:
```bash
sed 's/,/\t/g' squirrel-census.csv > squirrel-census.tsv
```

The `sed` command performs stream editing. `s/,/\t/g` substitutes commas with tabs globally (all occurrences in each line).

**Method 3: Using `awk`**

Convert CSV to TSV using awk:
```bash
awk 'BEGIN { FS=","; OFS="\t" } {$1=$1; print}' squirrel-census.csv > squirrel-census.tsv
```

Approach:
- `BEGIN { FS=","; OFS="\t" }` sets the input field separator to comma and output field separator to tab
- `$1=$1` forces awk to rebuild the record with the new separator
- `print` outputs the modified line

**Method 4: Using Python with string replace**

Create a Python script `csv_to_tsv_simple.py`:
```python
#!/usr/bin/env python3
import sys

# Get input and output filenames from command line arguments
if len(sys.argv) != 3:
    print("Usage: python3 csv_to_tsv_simple.py <input.csv> <output.tsv>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Read CSV file as text and convert to TSV
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        # Replace commas with tabs
        tsv_line = line.replace(',', '\t')
        outfile.write(tsv_line)
```

Run the script:
```bash
python3 csv_to_tsv_simple.py squirrel-census.csv squirrel-census.tsv
```

**Explanation:**
- The script accepts input and output filenames as command-line arguments
- `open(input_file, 'r')` opens the CSV file for reading as a text file
- `open(output_file, 'w')` opens the TSV file for writing
- `line.replace(',', '\t')` replaces commas with tabs in each line
- `outfile.write(tsv_line)` writes the converted line to the output file
- The `with` statement ensures files are properly closed after processing

**Method 5: Using Python with pandas**

Create a Python script `csv_to_tsv_pandas.py`:
```python
#!/usr/bin/env python3
import pandas as pd
import sys

# Get input and output filenames from command line arguments
if len(sys.argv) != 3:
    print("Usage: python3 csv_to_tsv_pandas.py <input.csv> <output.tsv>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Read CSV file
df = pd.read_csv(input_file)

# Write as TSV (tab-separated)
df.to_csv(output_file, sep='\t', index=False)

print(f"Conversion complete! {input_file} -> {output_file}")
```

Run the script:
```bash
python3 csv_to_tsv_pandas.py squirrel-census.csv squirrel-census.tsv
```

**Explanation:**
- `pandas.read_csv()` reads the CSV file, handling quoted fields and edge cases automatically
- `df.to_csv(sep='\t')` writes the data with tab separators
- `index=False` prevents writing row indices to the output file
- This method is more robust for CSV files with quoted fields containing commas
- Command-line arguments make the script reusable for any CSV/TSV conversion

**Verify the conversion:**

Check that the TSV file was created correctly:
```bash
head -n 3 squirrel-census.tsv
```

**Explanation:** View the first 3 lines to verify the tabs are in place. You can also use `cat -A` to see tab characters as `^I`:
```bash
head -n 1 squirrel-census.tsv | cat -A
```

### Working with JSON files

#### CLI: jq

Core Concepts to Learn About jq

- Everything is a Filter: A fundamental concept is that a jq program is a "filter". This filter takes a JSON input (data stream) and produces a JSON output. Even a simple literal value like "hello" or a number like 42 is considered a filter that produces that value as output.

- The Identity Filter (.): The simplest, but most important, filter is the identity filter, represented by a single dot (.). It takes the input and produces it unchanged as output (by default, pretty-printed). This is your starting point for nearly all jq operations.

- JSON Data Structures: A solid grasp of basic JSON terminology is crucial.

    - Objects: Enclosed in curly braces ({}) and store data as name-value pairs. You access properties using the . syntax (e.g., .name, .user.id).

    - Arrays: Enclosed in square brackets ([]) and store an ordered list of values. You can access elements by index (e.g., .[0]) or iterate over all elements using [].

- Piping (|) and Chaining Filters: jq is designed to work seamlessly within Unix pipelines. The output of one filter can be piped as input to the next filter using the pipe symbol (|), allowing for complex transformations to be built from simple, composable operations.

- Data Extraction and Transformation: Learn to use built-in filters and functions to:

    - Extract specific fields (e.g., .user.name).
    
    - Filter data based on conditions (e.g., using select()).

    - Create new objects and arrays (e.g., {"new_name": .old_name}).

    - Use built-in functions like length, keys, map, add, etc., to manipulate data.

- Iterating Arrays: The [] filter is essential for processing arrays. When applied to an array, it produces each element of the array as a separate output to the next filter in the pipeline, rather than the entire array at once. This enables operations on individual items within a list. 

#### Python: requests and json packages

### Data Cleaning Exercises

In this section, we'll practice cleaning the squirrel census CSV data using Linux CLI commands. Data cleaning is an essential step before analysis to ensure data quality and consistency.

**Exercise 1: Identify and count empty fields**

Find rows with empty values in a specific column:
```bash
awk -F',' '$2 == "" {print NR, $0}' squirrel-census.csv | head -20
```

**Explanation:**
- `awk -F','` sets comma as the field separator
- `$2 == ""` checks if the second column is empty
- `NR` is the current row number
- `$0` prints the entire row
- Count empty fields: `awk -F',' '$2 == ""' squirrel-census.csv | wc -l`

**Exercise 2: Remove duplicate rows**

Identify and remove duplicate rows:
```bash
# First, identify duplicates
sort squirrel-census.csv | uniq -d | head -10
```

**Explanation:**
- `sort` sorts all rows (duplicates will be adjacent)
- `uniq -d` shows only duplicate lines
- To remove duplicates and save: `sort squirrel-census.csv | uniq > squirrel-census-unique.csv`

**Exercise 3: Filter rows by date range**

Extract rows where a date column falls within a specific range:
```bash
awk -F',' '$1 >= "2018-10-01" && $1 <= "2018-10-31" {print}' squirrel-census.csv > squirrel-census-october.csv
```

**Explanation:** Adjust the date column index (`$1`) and date range based on your data structure.

**Exercise 4: Count unique values in a column**

Count how many unique values exist in a specific column:
```bash
cut -d',' -f5 squirrel-census.csv | sort | uniq | wc -l
```

**Explanation:**
- `cut -d',' -f5` extracts column 5
- `sort` sorts the values
- `uniq` removes duplicates
- `wc -l` counts the unique values

**Exercise 5: Replace specific values**

Replace a specific value throughout the file:
```bash
sed 's/OldValue/NewValue/g' squirrel-census.csv > squirrel-census-replaced.csv
```

**Explanation:** `sed` substitutes all occurrences of "OldValue" with "NewValue" globally (`g` flag).

**Additional Resources:**

For more advanced data cleaning techniques, explore these Kaggle tutorials:

1. <a href="https://www.kaggle.com/alexisbcook/handling-missing-values" target="_blank" rel="noopener noreferrer">Handling Missing Values</a>
2. <a href="https://www.kaggle.com/alexisbcook/scaling-and-normalization" target="_blank" rel="noopener noreferrer">Scaling and Normalization</a>
3. <a href="https://www.kaggle.com/alexisbcook/parsing-dates" target="_blank" rel="noopener noreferrer">Parsing Dates</a>
4. <a href="https://www.kaggle.com/alexisbcook/character-encodings" target="_blank" rel="noopener noreferrer">Character Encoding</a>
5. <a href="https://www.kaggle.com/alexisbcook/inconsistent-data-entry" target="_blank" rel="noopener noreferrer">Inconsistent Data</a>


### JSON - JavaScript Object Notation

Let's move on to JSON files.

Some iterations to try using the `jq` tool in the command-line:

Filter the `mock_data.json` file containing "flat", non-nested data.
```
cd /root/course/01-data/
cat mock_data.json
cat mock_data.json | jq -r .[]
cat mock_data.json | jq -r .[] | jq ."dob"
cat mock_data.json | jq -r .[] | jq ."dob" | grep "1998"
cat mock_data.json | jq -r .[] | jq ."dob" | grep "1998" | wc -l
```

Filter the `mock_data_nested.json` file containing nested data.
```
cd /root/course/01-data/
cat mock_data_nested.json
cat mock_data_nested.json | jq ."healthChecks"
cat mock_data_nested.json | jq ."healthChecks" | jq .[]."delaySeconds"
cat mock_data_nested.json | jq ."healthChecks" | jq -r .[]."delaySeconds"
```

```
cd /root/course/01-data/
cat mock_data_nested.json | jq ."container"
cat mock_data_nested.json | jq ."container" | jq ."volumes"
cat mock_data_nested.json | jq ."container" | jq ."volumes" | jq -r .[]."hostPath"
```

### Using Python to Parse JSON

The above example can easily be implemented in Python.

Create a Python script `extract_hostpath.py`:
```python
#!/usr/bin/env python3
import json

with open('mock_data_nested.json', 'r') as f:
    data = json.load(f)

for volume in data['container']['volumes']:
    print(volume['hostPath'])
```

Run the script:
```bash
python3 extract_hostpath.py
```

Notice the `-r` flag to toggle "raw" output versus quote-wrapped output.

Explore <a href="https://jqplay.org" target="_blank" rel="noopener noreferrer">jq play</a> for more lessons, inputs, filters, etc.

### csv

```
cat mock_data.csv
```

Note that the 6 columns are separated by 5 commas. Fields that must contain a comma should be quote-enclosed.

### tsv

Like CSV files separated by commas, tab-separated files are delimited by tabs. This can fool the naked eye, and throw off import
processes when stray tabs are inserted into the data fields.

To convert TSV to CSV, or vice versa, use a text search+replace function such as `awk`, `tr`, or a good IDE/text editor:

#### tr
```
tr '\t' ',' < file.tsv > file.csv
```

#### sed
```
sed 's/'$'\t''/,/g' file.tsv > file.csv
```

#### awk
```
awk 'BEGIN { FS="\t"; OFS="," } {$1=$1; print}' file.tsv > file.csv
```

### xml

Structured data. Note that every record, and every data field within each record, is fully wrapped in markup that is opened and closed:

```xml
<dataset>
  . . .
  <record>
    <id>97</id>
    <first_name>Tamarra</first_name>
    <last_name>Jeannaud</last_name>
    <email>tjeannaud2o@fema.gov</email>
    <ip_address>26.106.176.174</ip_address>
    <dob>11/19/1981</dob>
  </record>
  <record>
    <id>98</id>
    <first_name>Korney</first_name>
    <last_name>Hazlegrove</last_name>
    <email>khazlegrove2p@wsj.com</email>
    <ip_address>218.117.101.96</ip_address>
    <dob>01/06/1981</dob>
  </record>
  . . .
</dataset>
```

### sql

`cat` and `head` and `tail` the SQL snippet. Notice that each line consists of an isolated query.
The SQL file is therefore not a bulk insert statement (not properly) but a concatenated series of independent
SQL statements. This is a best practice so that any single line that triggers a failure can be more
easily identified and the previous inserts will have succeeded.

```
INSERT INTO mock_data_tbl (id, first_name, last_name, email, ip_address, dob) VALUES (1, 'Berkley', 'Annon', 'bannon0@accuweather.com', '193.95.255.138', '10/20/1991');
INSERT INTO mock_data_tbl (id, first_name, last_name, email, ip_address, dob) VALUES (2, 'Doro', 'Morse', 'dmorse1@moonfruit.com', '170.67.183.172', '12/01/1995');
INSERT INTO mock_data_tbl (id, first_name, last_name, email, ip_address, dob) VALUES (3, 'Charmain', 'Halden', 'chalden2@europa.eu', '170.112.37.136', '03/03/1982');
INSERT INTO mock_data_tbl (id, first_name, last_name, email, ip_address, dob) VALUES (4, 'Allissa', 'Wakefield', 'awakefield3@usgs.gov', '23.46.25.161', '10/05/1988');
```

## Working with remote data

### Fetch Remote Data using `curl` and `jq`

#### Replace USER with your GitHub username
```
curl https://api.github.com/users/USER/events
```

#### Scroll through events
```
curl https://api.github.com/users/nmagee/events | jq .[] | less
```

#### Filter out values:
```
curl https://api.github.com/users/nmagee/events | jq .[].id
curl https://api.github.com/users/nmagee/events | jq .[].payload.commits
curl https://api.github.com/users/nmagee/events | jq .[].payload.commits | jq .[].message
```

#### Format output:
```
curl 'https://api.github.com/repos/stedolan/jq/commits'
curl 'https://api.github.com/repos/stedolan/jq/commits' \
   | jq '.[] | {message: .commit.message, name: .commit.committer.name}'
```

There are plenty of other examples in the tutorial at https://stedolan.github.io/jq/tutorial/

### Tools for Retrieving Data

`curl` - is a common Linux-based tool to fetch raw files. You've been using it in the exercises above.
```
curl https://www.virginia.edu/ > index.html
```

`wget` - another common Linux-based tool, similar to `curl`.
```
wget https://www.virginia.edu/
```

`http` - runs the HTTPie tool to fetch web resources:
```
http --head https://www.virginia.edu/
http --body https://www.virginia.edu/
```

Windows 10 and above come with `curl.exe` installed:
```
# example 1
curl.exe --output index.html --url https://superuser.com
# example 2
curl.exe -o index.html https://superuser.com
```

### Working with San Francisco Airport Passenger Data

In this exercise, we'll work with the San Francisco Airport Passenger Statistics dataset. The data is available as JSON from the Socrata Open Data API.

**Download the data:**
```bash
curl -o airports.json https://data.sfgov.org/api/views/rkru-6vcg/rows.json
```

**Exercise 1: View basic information with jq**

View the dataset name:
```bash
jq '.meta.view.name' airports.json
```

**Explanation:** The `.meta.view.name` path accesses the name field in the nested JSON structure.

**Exercise 2: Count the number of records**

Count how many data records are in the file:
```bash
jq '.data | length' airports.json
```

**Explanation:** 
- `.data` accesses the data array
- `| length` counts the number of elements in the array

**Exercise 3: View a sample record**

Look at the first data record:
```bash
jq '.data[0]' airports.json
```

**Explanation:** `.data[0]` accesses the first element (index 0) of the data array.

**Exercise 4: Extract a specific field**

Extract the operating airline from the first 10 records:
```bash
jq -r '.data[0:10][] | .[10]' airports.json
```

**Explanation:**
- `.data[0:10]` gets the first 10 records
- `.[10]` extracts the element at index 10 (operating airline)
- `-r` outputs raw strings without quotes

**Exercise 5: Using Python's json package**

Create a simple Python script `parse_airports.py`:
```python
#!/usr/bin/env python3
import json

# Load the JSON file
with open('airports.json', 'r') as f:
    data = json.load(f)

# Print basic information
print("Dataset name:", data['meta']['view']['name'])
print("Number of records:", len(data['data']))

# View the first record
print("\nFirst record:")
print(data['data'][0])

# Extract operating airline from first 10 records
print("\nOperating airlines (first 10 records):")
for i in range(10):
    airline = data['data'][i][10]  # Index 10 contains operating airline
    print(f"  Record {i+1}: {airline}")
```

Run the script:
```bash
python3 parse_airports.py
```

**Explanation:**
- `json.load()` reads and parses the JSON file into a Python dictionary
- `data['meta']['view']['name']` accesses nested dictionary values
- `len(data['data'])` counts the number of records
- `data['data'][i][10]` accesses a specific field in a specific record

## Advanced Concepts (Optional)

### Streaming Large Files

When working with very large files that don't fit in memory, you need to process them in chunks rather than loading everything at once. Python's `pandas` library supports chunking:

```python
import pandas as pd

# Process CSV in chunks
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process each chunk
    process(chunk)
```

For JSON files, use streaming parsers like `ijson`:

```python
import ijson

# Stream parse large JSON files
with open('large_file.json', 'rb') as f:
    parser = ijson.items(f, 'item')
    for item in parser:
        process(item)
```

### Schema Validation

Validating data against a schema ensures data quality and catches errors early. For JSON, use JSON Schema:

```python
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"}
    },
    "required": ["name", "age"]
}

jsonschema.validate(instance=data, schema=schema)
```

For CSV files, consider using libraries like `pandera` or `great_expectations` for data validation.

### Binary and Columnar Formats

For better performance with large datasets, consider binary formats:

- **Parquet**: Columnar storage format, excellent for analytics workloads. Supports compression and schema evolution.
- **Avro**: Row-based binary format with schema evolution support.
- **Protocol Buffers**: Google's language-neutral, platform-neutral serialization format.

These formats offer:
- Better compression ratios
- Faster read/write performance
- Schema evolution support
- Type safety

Example with Parquet:
```python
import pandas as pd

# Write to Parquet
df.to_parquet('data.parquet', compression='snappy')

# Read from Parquet
df = pd.read_parquet('data.parquet')
```

## Resources

### File Format Documentation

* <a href="https://www.json.org/json-en.html" target="_blank" rel="noopener noreferrer">JSON Specification</a> - Official JSON format specification
* <a href="https://datatracker.ietf.org/doc/html/rfc4180" target="_blank" rel="noopener noreferrer">CSV RFC 4180</a> - CSV format standard
* <a href="https://www.w3.org/XML/" target="_blank" rel="noopener noreferrer">XML Specification</a> - W3C XML documentation

### Tools and Libraries

* <a href="https://stedolan.github.io/jq/manual/" target="_blank" rel="noopener noreferrer">jq Manual</a> - Complete jq documentation and tutorial
* <a href="https://jqplay.org/" target="_blank" rel="noopener noreferrer">jq Play</a> - Interactive jq playground
* <a href="https://pandas.pydata.org/docs/" target="_blank" rel="noopener noreferrer">Pandas Documentation</a> - Python data manipulation library
* <a href="https://parquet.apache.org/" target="_blank" rel="noopener noreferrer">Apache Parquet</a> - Columnar storage format documentation

### Data Cleaning and Validation

* <a href="https://greatexpectations.io/" target="_blank" rel="noopener noreferrer">Great Expectations</a> - Data validation framework
* <a href="https://pandera.readthedocs.io/" target="_blank" rel="noopener noreferrer">Pandera</a> - Statistical data validation for pandas
* <a href="https://json-schema.org/" target="_blank" rel="noopener noreferrer">JSON Schema</a> - Schema validation for JSON

### API and Web Data

* <a href="https://httpie.io/docs" target="_blank" rel="noopener noreferrer">HTTPie Documentation</a> - Command-line HTTP client
* <a href="https://curl.se/docs/manual.html" target="_blank" rel="noopener noreferrer">curl Manual</a> - Complete curl documentation
* <a href="https://docs.github.com/en/rest" target="_blank" rel="noopener noreferrer">GitHub API Documentation</a> - Working with GitHub's REST API
