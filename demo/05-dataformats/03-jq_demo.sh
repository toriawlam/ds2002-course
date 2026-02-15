#!/bin/bash

DOGS="https://dogapi.dog/api/v2/breeds/"

echo "Download and parse raw JSON output"
curl $DOGS | jq -r

echo "The data of interest is contained as array in the 'data' key"
curl $DOGS | jq -r ".data"

echo "Get the length of the data array"
curl $DOGS | jq -r ".data | length"

echo "get subset of records in array (by index)"
curl $DOGS | jq -r ".data[0,2,-1]"

echo "Constructs a new JSON object with selected fields"
curl $DOGS | jq -r ".data[] | {name:.attributes.name, hypoallergenic:.attributes.hypoallergenic, life_max:.attributes.life.max}"

echo "filter data and return array of dog names that are hypoallergenic"
curl -s $DOGS | jq -r "[.data[] | select(.attributes.hypoallergenic == true) | .attributes.name]"