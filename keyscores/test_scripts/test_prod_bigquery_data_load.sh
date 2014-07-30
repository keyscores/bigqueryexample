#!/bin/bash
echo "Load Cloud Storage CSV Files into BigQuery"
SERVER_URL=http://kinetic-physics-644.appspot.com python -m unittest test_bigquery_data_loading
