#!/usr/bin/env python

import requests
import json
import pandas as pd
import sys
import logging
import os

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[console_handler])

# should include an if __name__ == "__main__":
URL = "http://api.open-notify.org/iss-now.json"

def parse_args():
	try:
		csv_file = sys.argv[1]
	except IndexError:
		logging.error(f"Usage: python {sys.argv[0]} <csv_file>")
		sys.exit(1)
	return csv_file

def extract(url):
	logging.info(f"Getting data from {url}")
	try:
		response = requests.get(url)
		response.raise_for_status()
		data = response.json()
		return data
	
		logging.info(f"Extracted raw data and saved to {json_file}")
	except requests.exceptions.HTTPError as e:
		logging.error("HTTP error occurred:", e)
	except requests.exceptions.RequestException as e:
		logging.error("A request error occurred:", e)
	except Exception as e:
		logging.error("An unexpected error occurred:", e)

def transform(data):
	# transforms into a pandas dataframe
	logging.info("Transforming into a Pandas dataframe")
	
	df = pd.DataFrame([data])
	df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

	return df

def load(df, csv_file):
	if os.path.exists(csv_file):
		# csv file first, df second
		df_existing = pd.read_csv(csv_file)
		df_combined = pd.concat([df_existing, df], ignore_index=True)
		df_combined.to_csv(csv_file, index=False)
		logging.info(f"Loaded transformed data (saved to {csv_file})")
	else:
		df.to_csv(csv_file)
		logging.info(f"Create CSV file (saved to {csv_file})")

if __name__ == "__main__":
    csv_file = parse_args()
    data = extract(URL)
    df = transform(data)
    load(df, csv_file)
