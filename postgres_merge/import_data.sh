#!/bin/bash
DATABASE=postgresql+psycopg2://keyscores:1234@localhost:5434/keyscores
CSVFILE=$1
CONNECTOR=test
echo "Import data from $CSVFILE into $DATABASE with connector name $CONNECTOR"
python import.py --postgres ${DATABASE} --filenames ${CSVFILE} --connector ${CONNECTOR} --connector-version 1
