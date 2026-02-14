# Scripting in Python

The goal of this activity is to familiarize you with scripting in Python. Python scripting is essential for automating tasks, processing data, orchestrating workflows, and building reusable tools that can save time and reduce errors.

> **Note:** Work through the examples below in your terminal (Codespace or local), experimenting with each command and its various options. If you encounter an error message, don't be discouraged—errors are learning opportunities. Reach out to your peers or instructor for help when needed, and help each other when you can. 

If the initial examples feel like a breeze, challenge yourself with activities in the *Advanced Concepts* section and explore the resource links at the end of this post.

* Start with the **In-class Exercises**.
* Continue with the **Additional Practices** section on your own time. 
* Optional: Explore the **Advanced Concepts** if you wish to explore Python scripting in more depth.

## In-class exercises

Scripting in `python` is fairly similar to bash, but it has a lot more functionality in 
terms of libraries, classes, functions, etc. A few things to note:

- Unlike `bash`, it is not as easy to pass `$1`, `$2` parameters in the command-line. Refer to <a href="https://stackabuse.com/command-line-arguments-in-python/" target="_blank" rel="noopener noreferrer">Command line arguments in Python</a> for a basic tutorial.

- Python can invoke shell scripts in other languages.

- Python has many better options for conditional logic, error handling, and logging.

- Whereas `bash` and other low-level tools (`grep`, `sed`, `awk`, `tr`, `perl`, etc.) can parse 
plain-text "flat" files fairly efficiently, Python can ingest a data file and load it 
into memory for much more complex transformations. A library like `pandas` can use 
dataframes like a staging database for you to query, scan, count, etc. Here's a great [pandas
tutorial](https://www.kaggle.com/sohier/tutorial-accessing-data-with-pandas) on Kaggle.

If you want to use JupyerLab, follow the instructions for starting [JupyterLab in Codespaces](../../setup/codespace-jl.md) or [JypterLab on UVA's HPC system](../../setup/hpc.md#login-via-web-browser).

**While JupyterLab is a great tool to get started with Python, you should also spend time writing standalone Python scripts that can be executed from the command line.**

### Running a Python script

1. Open a terminal window.
2. In the terminal run:
    ```bash
    python3 my_script.py # add command line args as needed if the script is written to handle them.
    ```

### Parsing command line arguments

Use `sys.argv` to access command-line arguments:

```python
import sys

# sys.argv[0] is the script name
# sys.argv[1] is the first argument
if len(sys.argv) > 1:
    filename = sys.argv[1]
    print(f"Processing file: {filename}")
else:
    print("Error: Please provide a filename")
```

### Reading txt files

Read a text file line by line:

```python
with open('file.txt', 'r') as f:
    for line in f:
        print(line.strip())
```

### Writing text files

Write content to a text file:

```python
with open('output.txt', 'w') as f:
    f.write("Hello, World!\n")
    f.write("This is a new line.")
```

### Reading csv and tsv files with pandas

Read CSV and TSV files into a DataFrame:

```python
import pandas as pd

# Read CSV file
df = pd.read_csv('mock_data.csv')

# Read TSV file
df = pd.read_csv('mock_data.tsv', sep='\t')
```

### Writing csv and tsv files with pandas

Write a DataFrame to CSV or TSV:

```python
import pandas as pd

# Read existing data
df = pd.read_csv('mock_data.csv')

# Write to CSV
df.to_csv('new_mock_data.csv', index=False)

# Write to TSV
df.to_csv('new_mock_data.tsv', sep='\t', index=False)
```

### Grouping and filtering data with pandas

Filter and group data:

```python
import pandas as pd

# Read the data first
df = pd.read_csv('mock_data.csv')

# Filter rows (example: filter by first name)
filtered = df[df['first_name'] == 'Jereme']

# Group by column and count
grouped = df.groupby('last_name').size()
```

### Reading json files

Read JSON data from a file:

```python
import json

with open('mock_data.json', 'r') as f:
    data = json.load(f)
```

### Writing json files

Write data to a JSON file:

```python
import json

data = {'name': 'Alice', 'age': 30}
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### From dictionaries to json and back

Convert between dictionaries and JSON strings:

```python
import json

# Read JSON file into a dictionary
with open('mock_data.json', 'r') as f:
    data = json.load(f)

# Dictionary to JSON string
json_str = json.dumps(data[0])  # Convert first item to string

# JSON string to dictionary
my_dict = json.loads(json_str)
```

### Accessing API endpoints with request

Make HTTP requests to APIs:

```python
import requests

# Make a GET request to a public API
response = requests.get('https://restcountries.com/v3.1/all?fields=name,capital,population')
data = response.json()
print(f"Fetched {len(data)} countries")
```

### Exception handling

Handle errors gracefully using try/except blocks:

```python
import json

# Handle file I/O errors
try:
    with open('mock_data.json', 'r') as f:
        data = json.load(f)
    print(f"Successfully loaded {len(data)} records")
except FileNotFoundError:
    print("Error: File not found")
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON format - {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

**Note:** The ordering of the exception clauses goes from specific to more general.

**Great, you are ready to continue with [Lab 03 - Scripting](../../labs/03-scripting/README.md). Start working on Script 2 in that lab.**

## Additional Practice

1. Write a primary script in `bash` that does two things:
   - Invokes a `bash` script to retrieve the log file found in `retrieve-file.sh`.
   - Invokes a `python3` script to parse that file and write the output.

Explore the Python script in [this folder](.)

## Advanced Concepts (Optional)

### Command line arguments with argparse

Use `argparse` for more robust command-line argument parsing:

```python
import argparse

parser = argparse.ArgumentParser(description='Process some files')
parser.add_argument('filename', help='Input file to process')
parser.add_argument('-o', '--output', help='Output file name')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
args = parser.parse_args()

print(f"Processing {args.filename}")
if args.output:
    print(f"Output will be written to {args.output}")
```

### List comprehension

Create lists more concisely using list comprehensions:

```python
# Traditional approach
squares = []
for x in range(10):
    squares.append(x**2)

# List comprehension
squares = [x**2 for x in range(10)]

# With condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

### Working with environment variables

Access and set environment variables in Python:

```python
import os

# Get an environment variable
github_user = os.getenv('GITHUB_USER', 'default_user')

# Set an environment variable (for current process)
os.environ['MY_VAR'] = 'my_value'

# Check if variable exists
if 'GITHUB_USER' in os.environ:
    print(f"GitHub user: {os.environ['GITHUB_USER']}")
```

### Subprocess module

Run shell commands from Python:

```python
import subprocess
import sys

# Run a command and capture output
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)

# Run with error handling
try:
    result = subprocess.run(['python3', 'script.py'], check=True, capture_output=True, text=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}", file=sys.stderr)
```

## Resources

<a href="https://stackabuse.com/command-line-arguments-in-python/" target="_blank" rel="noopener noreferrer">Command line arguments in Python</a>
<a href="https://www.kaggle.com/sohier/tutorial-accessing-data-with-pandas" target="_blank" rel="noopener noreferrer">Pandas tutorial</a> on Kaggle.

