#!/usr/bin/env python

import requests
import json
import pandas as pd
import sys
import logging
import os
import mysql.connector

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "iss"

db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)
cursor = db.cursor()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[console_handler])

# should include an if __name__ == "__main__":
URL = "http://api.open-notify.org/iss-now.json"

# def parse_args():
# 	try:
# 		db = mysql.connector.connect(host=DBHOST,user=DBUSER,password=DBPASS,database=DB)
#         return db
# 	except mysql.connector.Error as err:
# 		logging.error(f"Database connection failed: {err}")
#         raise

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

def load(df,reporter_id):
	try:
		message = df["message"].iloc[0]
		position = df["iss_position"].iloc[0]

		latitude = position['latitude']
		longitude = position['longitude']
		timestamp = df["timestamp"].iloc[0].strftime("%Y-%m-%d %H:%M:%S")

		query = "insert into locations (message, latitude, longitude, timestamp, reporter_id) values (%s,%s,%s,%s,%s)"
		
		cursor.execute(query,(message,latitude,longitude,timestamp,reporter_id))
		db.commit()
	except mysql.connector.Error as err:
		logging.error("Insert failed: ", err)
		raise

def register_reporter(table,reporter_id, reporter_name):
	# query the reports table to check if reporter_id exists
	# if reporter_id doesn't exist, insert new record with reporter_id and reporter_name
	try:

		query = "select 1 from reporters where reporter_id = %s limit 1"
		cursor.execute(query,(reporter_id,))
		result = cursor.fetchone()

		if result is None:
			query = "insert into reporters (reporter_id, reporter_name) values (%s,%s)"
			cursor.execute(query,(reporter_id,reporter_name))
		else:
			query = "update reporters set reporter_name = %s where reporter_id = %s"
			cursor.execute(query, (reporter_name, reporter_id))
		db.commit()
	except mysql.connector.Error as err:
		logging.error("Reporter registration failed: ", err)
		raise


if __name__ == "__main__":
	try:
		# db = parse_args()
		cursor = db.cursor()
		register_reporter('reporters','kze4za','Victoria Lam')
		data = extract(URL)
		df = transform(data)
 		load(df, 'kze4za')
		db.commit()
	except Exception as e:
        logging.error(f"Program failed: {e}")

	
    
    
