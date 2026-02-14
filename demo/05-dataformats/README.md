# Demo 05: ETL Pipeline - Extract & Transform

Live coding demonstration of ETL (Extract, Transform, Load) pipeline basics using real-world country data from a public API.

**Concepts**: Simple API requests, converting csv/tsv files, JSON parsing, data extraction, transformation, loading

---

## Working with CSV and TSV files on the command line

CSV and TSV files are universal file formats for storing tabular data (think spreadsheets) in clear text formats.

Let's download the squirrel census data of New York City and save it as `squirrel-census.csv`:
```bash
curl -o squirrel-census.csv https://data.cityofnewyork.us/api/views/ej9h-v6g2/rows.csv
```

### Filtering Rows

To filter a block of rows 50-100 we can pipe `head` and `tail` like so:
```bash
head -100 squirrel-census.csv | tail -50
```

For a more flexible approach we can use `sed`

```bash
sed -n '51,101p' squirrel-census.csv > squirrel-census-rows50-100.csv
```

### Filtering Columns

Extract specific columns using `cut`:

```bash
cut -d ',' -f 1,2,3 squirrel-census.csv > squirrel-census-first3cols.csv
```

Approach:
- `cut` extracts specific columns from a file
- `-d','` sets the delimiter to comma
- `-f1,2,3` selects the first, second, and third columns
- The output is redirected to a new file

### Converting between CSV and TSV

The only difference between CSV and TSV file formats is the delimiter that separates column values, i.e., a `,` for CSV and `<tab>` for TSV files.

The `tr` command is very versatile for replacing characters or text elements.

We can use it to convert CSV to TSV like so:

```bash
tr ',' '\t' < squirrel-census.csv > squirrel-census.tsv
```

`tr ',' '\t'` substitutes commas with tabs (`\t`) globally (all occurrences in each line). Note the redirection of input `<` and output `>`.

If you reverse the order to `tr '\t' ','` you can convert from TSV to CSV. 

## Working with CSV/TSV files in Python

The simplest way to do this is with pandas.

```python
import pandas as pd

df = pd.read_csv(my_csv_file, sep=",")
df.to_csv(my_tsv_file, sep="\t", index=False)
```

Or the reverse:
```python
import pandas as pd

df = pd.read_csv(my_tsv_file, sep="\t")
df.to_csv(my_csv_file, sep=",", index=False)
```

## Working with JSON files on the command line

The `jq` tool is extremely versatile for handling JSON files via command line interface (CLI).

For this example we use the public [Dog API](https://dogapi.dog). It provides a fun list of features for dog breeds. The URL is `https://dogapi.dog/api/v2/breeds/`.

Let's set an environment variable so we don't have to remember the URL

```bash
export DOGS="https://dogapi.dog/api/v2/breeds/"
```

```bash 
curl -s https://dogapi.dog/api/v2/breeds/
```

or shorter:
```bash
curl $DOGS
```

Let's use `jq` to parse the unformatted JSON data.

```bash
curl $DOGS | jq -r
```

Note how we pipe the downloaded data into the `jq` command. The `-r` flag tells it to provide the raw data output. That's overwhelming. Let's inspect the data structure in more detail.

```bash
curl -s https://dogapi.dog/api/v2/breeds/ | jq -r | head
```

Output
```json
{
  "data": [
    {
      "id": "036feed0-da8a-42c9-ab9a-57449b530b13",
      "type": "breed",
      "attributes": {
        "name": "Affenpinscher",
        "description": "The Affenpinscher is a small and playful breed of dog that was originally bred in Germany for hunting small game. They are intelligent, energetic, and affectionate, and make excellent companion dogs.",
        "life": {
          "max": 16,
```

**Understanding JSON Structure:**
- **`{}` (curly braces)** = Object/Dictionary - contains key-value pairs (like a Python dictionary)
  - Example: `{"name": "Affenpinscher", "type": "breed"}` - has named fields
- **`[]` (square brackets)** = Array/List - contains an ordered list of values (like a Python list)
  - Example: `["item1", "item2", "item3"]` - just a list of items

**JSON Keys:**
- **Keys** are the names/labels in a JSON object (always strings, in quotes)
- Keys are followed by a colon `:` and then their value
- Example: In `{"name": "Affenpinscher", "type": "breed"}`, `"name"` and `"type"` are keys
- You access values using their keys: `.name` or `["name"]` in jq
- Keys can have nested objects as values: `"attributes": {...}` means the key `attributes` contains another object

In the output above:
- The outer `{` starts a JSON object with a `"data"` key
- The `[` after `"data":` starts an array of breed objects
- Each breed is itself an object `{...}` with nested objects like `"attributes": {...}` 

Note the `"data": [` which indicates that `data` holds an array/list of entries. 

Getting length of JSON array in `data`
```bash
curl $DOGS | jq '.data | length'
```

Getting list of top-level keys for the first record in `data[0]`
```bash
curl $DOGS | jq '.data[0] | keys'
```

Getting list of nested keys within `attributes` for the first record
```bash
curl $DOGS | jq '.data[0].attributes | keys'
```

Getting all keys at all nesting levels (recursive)
```bash
curl $DOGS | jq '.data[0] | paths(scalars) as $p | {path: $p, value: getpath($p)}'
```

Let's take a look at the first record. 

```bash
curl -s https://dogapi.dog/api/v2/breeds/ | jq -r ".data[0]"
```

Output:
```json
{
  "id": "036feed0-da8a-42c9-ab9a-57449b530b13",
  "type": "breed",
  "attributes": {
    "name": "Affenpinscher",
    "description": "The Affenpinscher is a small and playful breed of dog that was originally bred in Germany for hunting small game. They are intelligent, energetic, and affectionate, and make excellent companion dogs.",
    "life": {
      "max": 16,
      "min": 14
    },
    "male_weight": {
      "max": 5,
      "min": 3
    },
    "female_weight": {
      "max": 5,
      "min": 3
    },
    "hypoallergenic": true
  },
  "relationships": {
    "group": {
      "data": {
        "id": "f56dc4b1-ba1a-4454-8ce2-bd5d41404a0c",
        "type": "group"
      }
    }
  }
}
```

You can see that each entry contains a nested structure of smaller JSON formatted data. We can drill down by chaining the keys with the `.` character like so:

Extract a single nested value from the first breed record.
```bash
curl $DOGS | jq -r ".data[0].attributes.name"
```

Create a new JSON object with selected fields from the first breed record.
```bash
curl $DOGS | jq -r ".data[0] | {name: .attributes.name, max_life:.attributes.life.max}"
```

Extract the same fields from both the first and last breed records in the array.
```bash
curl $DOGS | jq -r ".data[0,-1] | {name: .attributes.name, max_life:.attributes.life.max}"
```

Extract the same fields from all breed records in the array.
```bash
curl $DOGS | jq -r ".data[] | {name: .attributes.name, max_life:.attributes.life.max}"
```

Filtering data: Get only hypoallergenic breeds (where `hypoallergenic` is `true`).
```bash
curl $DOGS | jq '.data[] | select(.attributes.hypoallergenic == true) | {name: .attributes.name}'
```

Filtering data: Get breeds with maximum life expectancy greater than 15 years.
```bash
curl $DOGS | jq '.data[] | select(.attributes.life.max > 15) | {name: .attributes.name, max_life: .attributes.life.max}'
```

Saving restructured JSON to file
```bash
curl $DOGS | jq '.data[] | {name: .attributes.name, max_life:.attributes.life.max}' > dogs_clean.json
```

Reading JSON from file
```bash
jq -r <  dogs_clean.json
```


---

## Demo 2: ETL Demo with JSON data in Python

**Objective:**
- "ETL stands for Extract, Transform, Load - the foundation of data engineering"
- "Today we'll extract data from an API and transform it from nested JSON to a clean CSV"
- "This is what data engineers do every day - take messy data, reshape them, and make them usable"

### Prerequisites
You need to install a few Python packages for this demo:
```bash
pip install requests pandas
```

If you get a warning or error, try:
```bash
pip install --user requests pandas
```

Note: `csv` and `json` are built-in Python modules and don't need to be installed.

You can find the full code example of this demo in `05-etl_demo.py`. Run it like this:

```bash
python 05-etl_demo.py dogs_complete.json dogs_clean.csv
```

### 0. Scaffolding our Program

Our starting point for this demo is `04-etl_demo_stub.py`. In the interest of time, we define variables for `json_file` and `csv_file` for this demo. We also keep the code simple without error handling. Please review `05-etl_demo.py` after the demo for a more complete and robust example.

```python
import requests
import json
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = "https://dogapi.dog/api/v2/breeds/"
json_file = "dogs_complete.json"
csv_file = "dogs_clean.csv"
selected = ["attributes.name", "attributes.hypoallergenic", "attributes.life.max"]
```

### 1. Extract

```python
# Download data and parse as json
response = requests.get(URL)
logger.info(f"status: {response.status_code}")
data = response.json()
logger.info(f"top level keys: {list(data.keys())}")

# Save raw data (filename from command-line args)
with open(json_file, 'w') as f:
    json.dump(data, f, indent=2)
logger.info(f"Saved raw data to {json_file}")
```

The nested JSON structure: At the top level we have `data` with an array containing breed objects. Each object has a field with `attributes` nested inside.

**Key Concepts**: 
- It is generally advised to save raw data before transforming
- Use logging for better debugging and monitoring
- Error handling is important. APIs can fail, networks can timeout. See `04-etl_demo_stub.py` for catching exceptions.

### 2. Transform

Let's get the data into shape. In this example we're flattening the JSON, convert it into a spreadsheet-like dataframe, and select a subset of the columns of interest.

```python
import pandas as pd

# (Re)load raw data
with open(json_file, 'r') as f:
    raw_data = json.load(f)

# Extract data array if present
if 'data' in raw_data:
    breeds_data = raw_data['data']
else:
    breeds_data = raw_data if isinstance(raw_data, list) else [raw_data]

# Flatten nested JSON
df = pd.json_normalize(breeds_data)
```

Check the flattened dataframe column headers with `df.columns.values` or the top of the dataframe with `df.head`.

```python
# retaining only the columns of interest
df = df[selected]
df_clean = df.reset_index(drop=True)

logger.info(f"Transformed: {df_clean.shape[0]} rows × {df_clean.shape[1]} columns")
```

**Key Concepts:**
- The data is nested - `attributes` contains `name`, `life`, `weight`, etc. We flatten it using `json_normalize()` which turns nested objects into columns
- We filter columns to keep only what we need (containing 'name', 'hypoallergenic', 'weight', or 'life') - this reduces data size and complexity
- Notice how `attributes.name` in the JSON became `attributes.name` column (pandas preserves the path)
- Logging provides visibility into the transformation process
- For production, you'd add more cleaning: remove duplicates, fix data types, handle missing values. Logging helps track the process

> **Note**: Flattening nested data makes it easier to analyze, and selecting only needed columns reduces complexity. We will expand on that when working with SQL databases. But for some data the nested, hierarchical structure reflects important data relationships and therefore it may not always be appropriate to flatten. **As a data engineer you have to make that decision on a case-by-case basis.** 

### 3. Load

Now let's export the transformed data into a csv file. In later labs we will load the dataframe into a database.

```python
# Save clean data
df_clean.to_csv(csv_file, index=False)
logger.info(f"Saved clean data to {csv_file}")

# Log final summary
logger.info(f"Processed {len(df_clean)} records")
```

>**Note**: In the stub version, the CSV filename is defined as a variable. In `05-etl_demo.py`, it's specified via command-line arguments.

**Key Concepts:**
- CSV format is universal - works with Excel, databases, Python, R
- Compare: messy nested JSON → clean flat CSV with selected columns
- Logging gives us a record of what happened - important for debugging
- This is what we'll load into a database in the next lab

---

### Takeaways

1. **Extract**: Get data from source with error handling, save raw version, use logging
2. **Transform**: Flatten nested structures, select relevant columns, clean data
3. **Load**: Save to CSV format for analysis, log the process

For production code and to support reusability of our script, we want to reorganize the extract, transform, load operations into separate functions. Such modular design is a fundamental concept of data pipelines and follows software engineering best practices.

### Running the Demo

**Please review the `05-etl_demo.py` script and run it to see it in action.**
 
```bash
# Run the complete ETL pipeline
python 05-etl_demo.py dogs_complete.json dogs_clean.csv
```

The script will:
1. **Extract**: Download data from DOGS API and save to `dogs_complete.json`
2. **Transform**: Load JSON, flatten nested structure, and select columns containing "name", "hypoallergenic", "weight", or "life"
3. **Load**: Save cleaned data to `dogs_clean.csv` with logging output

### Files Created

After running the demo:
- `dogs_complete.json` - Original nested JSON data (filename from command-line)
- `dogs_clean.csv` - Clean, flat CSV with selected columns ready for analysis (filename from command-line)

---

### Common Questions

**Q: Why not transform directly without saving raw?**  
A: You might need to re-run transformations, or the API might change. Or for large data you may have to read it as a stream and save because it may not fit into your computers memory. See below.

**Q: What if the API requires authentication?**  
A: Add headers or API keys to the request: `requests.get(url, headers={'Authorization': 'Bearer token'})`

**Q: What about very large datasets?**  
A: Use Spark, dask dataframes, or cloud tools (AWS Glue, Azure Data Factory) instead of pandas.

**Q: How do you handle API errors?**  
A: Use try/except blocks with specific exception types (HTTPError, RequestException) and log errors. The demo shows basic error handling - production code would add retry logic.

---

### Resources

To familiarize yourself with handling CSV/TSV and JSON data, work through [Practice 05: Working with file formats and cleaning data](../../practice/05-dataformats/README.md). [Lab 04: Data Formats - ETL Pipeline Basics](../../labs/04-dataformats/README.md) also builds on these concepts.