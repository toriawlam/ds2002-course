#!/usr/bin/env python3

import os
import mysql.connector

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = os.environ.get('DB', 'media')

# In your terminal, define the following environment variables:
# export DBHOST='ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com'
# export DBUSER='ds2002'
# export DBPASS='<see AWS_RDS_CREDENTIALS.txt on Canvas>'
# export DB='media'  # optional, defaults to 'media'

db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)
cursor = db.cursor(dictionary=True)

query = "SELECT id, email, ip_address FROM MOCK_DATA LIMIT 5"
cursor.execute(query)
results = cursor.fetchall()

for row in results:
    print(f"ID: {row['id']}, Email: {row['email']}, IP: {row['ip_address']}")

cursor.close()
db.close()
