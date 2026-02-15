# Lab 04: Data Formats - ETL Pipeline Basics

The goal of this activity is to get you comfortable with building ETL (Extract, Transform, Load) pipelines—the foundation of data engineering. You will practice extracting data from APIs, transforming JSON into tabular formats, and loading data into files. Follow the steps below to create a Python script that demonstrates these fundamental data pipeline concepts.

Follow the steps below to build an ETL pipeline. You will develop one Python script in this lab that tracks the International Space Station. Commit your work to your `ds2002-course` repository and submit the URL to your repo for grading.

## Setup

For the Python scripts in this lab, you will need Python3 installed on your local system, or use Codespace.

Python3 should be available in your path. Use `which python3` to find the path. That path should be something like `/usr/bin/python3`

You will also need to install the `requests` and `pandas` libraries for Python. To do this, run this command:

```bash
pip install requests pandas
```

Depending on your account permissions you may get an error, preventing you from installing packages into the system's python environment. In such case, try this:

```bash
pip install --user requests pandas
```

The `--user` flag directs the installation into a personal package library in your home directory `~/.local`.

## Tracking the International Space Station

**The Case:** You've just been contacted by a space enthusiast group that's organizing a "Spot the ISS" event. They want to track the International Space Station's position over time to help participants know when and where to look in the sky. The group has been manually checking the ISS location API every few minutes and writing down coordinates—a tedious and error-prone process that's taking up all their time.

The event coordinator needs an automated system that can:
- Continuously fetch the ISS's current location from a public API
- Convert the raw JSON data into a readable, tabular format
- Build a historical record by appending each location reading to a CSV file
- Provide logging so they can track when data was collected

**Your Task:** Build a Python ETL pipeline that automatically extracts ISS location data, transforms it into a clean format, and loads it into a CSV file. This script will demonstrate the core ETL workflow—Extract, Transform, Load—which is the foundation of data engineering. You're not just writing code—you're building a real data pipeline that could help people spot the space station!

**Let's Build It:**

1. In the fork of your ds2002-course repository, create a new folder `mywork/lab4`.

2. Change to the `mywork/lab4` directory and create a new file `iss.py`.

3. The `iss.py` Python script should implement the following ETL workflow according to these specifications:

   a. The script should accept one command line argument. This argument defines the CSV output file to save the script's results to.  
   
   b. Your Python script should start with a shebang.
   
   c. Following the shebang, add all needed import statements.
   
   d. Following the import statements, the script should initialize a logger. See the scripts `logging_advanced.py` (in `practice/04-python`) or `05-etl_demo.py` (in `demo/05-dataformats`) for examples. The logger should output to the console.
   
   e. The script should contain an `if __name__ == "__main__":` block that contains a call to a function `main()`.

   f. The extract, transform, load operations should be implemented in **three separate functions**. These three functions should be called in sequence from within the `main` function. They define the core data pipeline. The overall code structure should be similar to `05-etl_demo.py` in `demo/05-dataformats`. Each function, including `main()` should have a doc string to document its purpose.
   
     * **extract function:** Downloads the JSON data from the API endpoint [http://api.open-notify.org/iss-now.json](http://api.open-notify.org/iss-now.json). You may want to save the raw JSON to a temporary file so you can inspect its structure. **Hint:** Check the API documentation at [http://open-notify.org/Open-Notify-API/ISS-Location-Now/](http://open-notify.org/Open-Notify-API/ISS-Location-Now/). The function should handle errors gracefully using try/except blocks. Take inspiration from `05-etl_demo.py` (in `demo/05-dataformats`). The function should return the parsed JSON data record.
   
     * **transform function:** Accepts a JSON data record (provided by the extract function) as a parameter and converts it into tabular format with `pandas`. The raw data's timestamp values are provided in seconds (UNIX time). Convert the timestamp into a more intuitive format like `YYYY-MM-DD HH:MM:SS`. **Hint:** Explore the documentation for `pd.to_datetime()`. The function should return the tabularized record, i.e., as a single row pandas DataFrame.
   
     * **load function:** Accepts two parameters: (1) a tabularized data record (e.g., in pandas DataFrame format), and (2) the name of the CSV file. The function **appends** the passed data record to the specified CSV file. Make sure that the CSV file is created the first time the script is run, and that the file is appended, not overwritten, for subsequent calls. Over time subsequent script executions will build a growing timeseries dataset. **Hint:** Explore the `os` and `pandas` packages. You can use `os.path.exists()` to check if a file exists, and `pd.concat()` to append data and then rewrite the CSV file.

   g. Add meaningful logging messages in each of your functions.

   h. Run your script at least 10 times; you can use a simple loop or run it manually. If you run the script in an automated loop you need to include a wait/sleep step of at least 1 second because the API is rate limited to 1 call per second (1 Hz). Your output CSV file should have at least 10 data rows. Include the CSV file in the `mywork/lab4` folder.

   **🎉 Success!** Your ETL pipeline is working! The space enthusiast group can now automatically track the ISS location over time. The CSV file will show a historical record of where the space station has been, making it easy to analyze patterns and help event participants know when to look up. Move on to the additional challenge, or submit your work!

   **⚡ Additional Challenge (Optional):**
   
   Your script impressed the group so much that they want to expand its capabilities! They're asking for a more robust version with enhanced logging:
   
   a. Update the logger to include both a `StreamHandler` to log to the console and a `FileHandler` to write to a log file simultaneously. This way, they can see real-time progress in the console while maintaining a permanent record in a log file.

With your ETL pipeline complete, you've successfully demonstrated the core workflow that data engineers use every day. You've learned how to:
- Extract data from REST APIs
- Transform nested JSON into flat, tabular formats
- Handle timestamps and data type conversions
- Load data incrementally by appending to files
- Implement proper logging for debugging and monitoring

This ETL pattern is the foundation for working with data pipelines, databases, and data warehouses. The skills you've practiced here will be essential as you move on to more complex data engineering tasks in the coming weeks.

## Submit your work

You created one script for this lab (`iss.py`) and a CSV data file. Both should be in a folder `ds2002-course/mywork/lab4` within your fork of the course repository. Add, commit, and push your work. Then submit the URL of your forked repo `ds2002-course/mywork/lab4` in the text box within Canvas.
