#!/usr/bin/env python
"""
ETL Demo: Extract and Transform Dog Breed Data
Live coding demonstration for ETL pipeline basics
"""

import requests
import json
import pandas as pd
import sys
import logging

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[console_handler])

URL = "https://dogapi.dog/api/v2/breeds/"

def parse_args():
    try:
        json_file = sys.argv[1]
        csv_file = sys.argv[2]
    except IndexError:
        logging.error(f"Usage: python {sys.argv[0]} <json_file> <csv_file>")
        sys.exit(1)
    return json_file, csv_file


def extract(url, json_file):
    """
    Extract: Get data from API and save raw JSON.
    Returns the number of records in the raw data.
    """
    logging.info(f"Getting data from {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status() # raise an exception for HTTP errors
        data = response.json()
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Extracted raw data and saved to {json_file}")
    except requests.exceptions.HTTPError as e:
        logging.error("HTTP error occurred:", e)
    except requests.exceptions.RequestException as e:
        logging.error("A request error occurred:", e)
    except Exception as e:
        logging.error("An unexpected error occurred:", e)


def transform(json_file, selected=["name", "hypoallergenic", "life.max"]):
    """
    Transform: Load raw JSON, flatten, and keep only selected fields.
    Returns a cleaned DataFrame.
    """
    logging.info("Cleaning and organizing data...")
    
    # Load raw data
    with open(json_file, 'r') as f:
        raw_data = json.load(f)
    
    # Extract data array if present
    if 'data' in raw_data:
        breeds_data = raw_data['data']
    else:
        breeds_data = raw_data if isinstance(raw_data, list) else [raw_data]
    
    # Flatten nested JSON
    logging.info("Flattening nested structure...")
    df = pd.json_normalize(breeds_data)
    #stripping attributes. from the column names
    df.columns = df.columns.str.replace('attributes.', '')
    
    # Select columns that contain any of the selected field names
    df = df[selected]
    logging.debug(f"Selected columns: {selected}")
    df_clean = df.reset_index(drop=True)
    
    logging.info(f"Transformed: {df_clean.shape[0]} rows × {df_clean.shape[1]} columns")
    
    return df_clean


def load(df, csv_file):
    """
    Load: Save transformed data to CSV and display summary.
    """
    # Save clean data
    df.to_csv(csv_file, index=False)
    logging.info(f"Loaded transformed data (saved to {csv_file})")


def main():
    """Run the complete ETL pipeline."""
    logging.info("ETL PIPELINE DEMO")

    # Parse command line arguments
    json_file, csv_file = parse_args()
    
    # Extract: Get data from API
    extract(URL, json_file)
    
    # Transform: Clean and organize data
    df = transform(json_file)
    
    # Load: Save to CSV and show summary
    load(df, csv_file)
    logging.info(f"Processed {len(df)} records")


# This block is executed only if the script is run directly, not imported as a module.
if __name__ == "__main__":
    main()

