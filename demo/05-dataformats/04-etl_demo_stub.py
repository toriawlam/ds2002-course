#!/usr/bin/env python
"""
ETL Demo: Extract and Transform Dog Breed Data
Live coding demonstration for ETL pipeline basics

This is a stub as starting point for the ETL demo.
"""

import requests
import json
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = "https://dogapi.dog/api/v2/breeds/"
json_file = "dogs_complete.json"
csv_file = "dogs_clean.csv"
selected = ["attributes.name", "attributes.hypoallergenic", "attributes.life.max"]