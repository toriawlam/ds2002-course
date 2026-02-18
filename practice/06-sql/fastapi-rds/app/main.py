#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from database import db
from mysql.connector import Error
import json
import decimal
from decimal import Decimal
import datetime

def Decoder(o):
    if isinstance(o, datetime.datetime):
        return str(o)
    elif isinstance(o, decimal.Decimal):
        return o.__str__()

app = FastAPI()

class Track(BaseModel):
    id: str
    telem_1: float
    telem_2: float
    longitude: float
    latitude: float
    created_on: str

@app.get("/")  # zone apex
def read_root():
    return {"Hello": "Grabbing DB data!"}

@app.get("/tracking/{year}/{month}")
def get_tracks(year: int, month: int):
    # Pay attention to dropped leading zeros in month values
    month_str = f"{year}-{month:02d}-%"
    # Perform a LIKE query with parameterized values
    query = "SELECT * FROM tracking WHERE created_on LIKE %s ORDER BY created_on"
    cursor = db.cursor(dictionary=True)
    try:
        # Execute query against cursor
        cursor.execute(query, (month_str,))
        # Fetch all results
        results = cursor.fetchall()
        # Pass data through the JSON encoder
        json_compatible_data = jsonable_encoder(results)
        return JSONResponse(content=json_compatible_data)
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
    
@app.post("/tracking/", status_code=201)
async def add_track(item: Track):
    # Get columnar values from submitted payload
    track_id = item.id
    telem_1 = item.telem_1
    telem_2 = item.telem_2
    longitude = item.longitude
    latitude = item.latitude
    created_on = item.created_on
    # Use parameterized query to prevent SQL injection
    query = "INSERT INTO tracking (id, telem_1, telem_2, longitude, latitude, created_on) VALUES (%s, %s, %s, %s, %s, %s)"
    record_data = (track_id, telem_1, telem_2, longitude, latitude, created_on)
    cursor = db.cursor()
    try:
        cursor.execute(query, record_data)
        # Commit the transaction
        db.commit()
        return {"created": "success", "id": track_id}
    except Error as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
