import os
import mysql.connector

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = os.environ.get('DB', 'ds3002')

# In your terminal, define the following environment variables:
# export DBHOST='ds3002-rds.cqee4iwdcaph.us-east-1.rds.amazonaws.com'
# export DBUSER='ds3002'
# export DBPASS='<see AWS_RDS_CREDENTIALS.txt on Canvas>'
# export DB='ds3002'  # optional, defaults to 'ds3002'

db = mysql.connector.connect(
    host=DBHOST,
    user=DBUSER,
    password=DBPASS,
    database=DB
)