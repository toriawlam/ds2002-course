#!/usr/bin/env python

import requests
import pandas as pd
import logging
import os
import mysql.connector

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "iss"

URL = "http://api.open-notify.org/iss-now.json"

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[console_handler])


def parse_args():
    try:
        db = mysql.connector.connect(
            host=DBHOST,
            user=DBUSER,
            password=DBPASS,
            database=DB
        )
        return db
    except mysql.connector.Error as err:
        logging.error(f"Database connection failed: {err}")
        raise


def extract(url):
    logging.info(f"Getting data from {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.HTTPError as e:
        logging.error("HTTP error occurred: %s", e)

    except requests.exceptions.RequestException as e:
        logging.error("Request error occurred: %s", e)

    except Exception as e:
        logging.error("Unexpected error occurred: %s", e)


def transform(data):
    logging.info("Transforming into a Pandas dataframe")

    df = pd.DataFrame([data])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    return df


def load(df, reporter_id, cursor, db):

    try:
        message = df["message"].iloc[0]
        position = df["iss_position"].iloc[0]

        latitude = position["latitude"]
        longitude = position["longitude"]

        timestamp = df["timestamp"].iloc[0].strftime("%Y-%m-%d %H:%M:%S")

        query = """insert into locations (message, latitude, longitude, timestamp, reporter_id) values (%s, %s, %s, %s, %s)"""

        cursor.execute(query, (message, latitude, longitude, timestamp, reporter_id))

        db.commit()

        logging.info("Inserted new ISS location")

    except mysql.connector.Error as err:
        logging.error("Insert failed: %s", err)
        raise

def register_reporter(table, reporter_id, reporter_name, cursor, db):

    try:
        query = "select 1 from reporters where reporter_id = %s limit 1"
        cursor.execute(query, (reporter_id,))
        result = cursor.fetchone()

        if result is None:
            query = "insert into reporters (reporter_id, reporter_name) values (%s,%s)"
            cursor.execute(query, (reporter_id, reporter_name))
            logging.info("Reporter registered")

        else:
            query = "update reporters set reporter_name = %s where reporter_id = %s"
            cursor.execute(query, (reporter_name, reporter_id))
            logging.info("Reporter already exists, updated name")

        db.commit()

    except mysql.connector.Error as err:
        logging.error("Reporter registration failed: %s", err)
        raise

if __name__ == "__main__":

    REPORTER_ID = "kze4za"
    REPORTER_NAME = "Victoria Lam"

    db = None
    cursor = None

    try:
        db = parse_args()
        cursor = db.cursor()

        register_reporter("reporters", REPORTER_ID, REPORTER_NAME, cursor, db)

        data = extract(URL)

        df = transform(data)

        load(df, REPORTER_ID, cursor, db)

    except Exception as e:
        logging.error(f"Program failed: {e}")

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()

        logging.info("Database connection closed")