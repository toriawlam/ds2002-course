#!/bin/bash

echo "Downloading squirrel census data..."
curl -o squirrel-census.csv https://data.cityofnewyork.us/api/views/ej9h-v6g2/rows.csv

echo "Displaying the first line of the squirrel census data..."
head -n 1 squirrel-census.csv

echo "Displaying the number of lines in the squirrel census data..."
wc -l < squirrel-census.csv

echo "Displaying the number of columns in the first line of the squirrel census data..."
head -n 1 squirrel-census.csv | tr ',' '\n' | wc -l

echo "Extracting and saving the first 11 lines of the squirrel census data..."
head -n 11 squirrel-census.csv > squirrel-census-sample.csv

echo "Extracting and saving the first 50 lines of the squirrel census data..."
sed -n '51,101p' squirrel-census.csv > squirrel-census-rows50-100.csv

echo "Extracting and saving the first 3 columns of the squirrel census data..."
cut -d',' -f1,2,3 squirrel-census.csv > squirrel-census-first3cols.csv

echo "Converting the squirrel census data to TSV format..."
tr ',' '\t' < squirrel-census.csv > squirrel-census.tsv
