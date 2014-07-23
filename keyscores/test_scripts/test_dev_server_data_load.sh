#!/bin/bash
echo "Load Country_and_Region.xlsx"
SERVER_URL=http://localhost:8080 python -m unittest test_data_loading
