#!/bin/bash
DATABASE=postgresql+psycopg2://keyscores:1234@localhost:5434/keyscores
CONNECTOR=test
CONNECTOR_VERSION=1
echo "Merge imported data from $1 into $DATABASE with connector name $CONNECTOR and version $CONNECTOR_VERSION"
python merge.py --postgres ${DATABASE} --filenames ${1} --connector ${CONNECTOR} --connector-version ${CONNECTOR_VERSION}