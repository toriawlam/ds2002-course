#!/usr/bin/env python3

import json
import os
import mysql.connector
from mysql.connector import Error
import decimal
from decimal import Decimal
import datetime

# In your terminal, define the following environment variables:
# export DBHOST='ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com'
# export DBUSER='ds2002'
# export DBPASS='<see AWS_RDS_CREDENTIALS.txt on Canvas>'
# export DB='khs3z_db'  # optional, defaults to 'khs3z_db'

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = os.environ.get('DB', 'khs3z_db')

db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)

year = 2020
month = 8

def Decoder(o):
    if isinstance(o, datetime.datetime):
        return str(o)
    if isinstance(o, decimal.Decimal):
        return o.__str__()

def get_logistics(year: int, month: int):
    # Use parameterized query to prevent SQL injection
    query = "SELECT * FROM logistics WHERE created_on LIKE %s ORDER BY created_on"
    month_str = f"{year}-{month:02d}-%"
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(query, (month_str,))
        results = cursor.fetchall()
        json_data = []
        for result in results:
            json_data.append(result)
        output = json.dumps(json_data, default=Decoder)
        print(output)
        return output
    except Error as e:
        print("MySQL Error:", str(e))
        return None
    finally:
        cursor.close()
        db.close()

# Run the script
if __name__ == '__main__':
    get_logistics(year,month)
