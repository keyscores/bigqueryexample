#!/bin/bash
export SERVER_URL=http://kinetic-physics-644.appspot.com
export BUCKET_NAME=keyscores_test
export CONTENT_TYPE=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
pytest test_cloud_storage_file_upload.py
