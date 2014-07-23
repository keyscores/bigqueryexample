#!/bin/bash
echo "Load Country_and_Region.xlsx"
SERVER_URL=http://kinetic-physics-644.appspot.com python -m unittest test_data_loading
