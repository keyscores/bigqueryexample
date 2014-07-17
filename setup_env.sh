#!/bin/sh

echo "Set up environment variables to use with Google Cloud Platform"
export PROJECT="kinetic-physics-644"
echo "PROJECT=$PROJECT"
export BUCKET_NAME="keyscores_test"
echo "BUCKET_NAME=$BUCKET_NAME"
export SERVER="http://localhost:8080"
echo "SERVER=$SERVER"
export PYTHONPATH=$PYTHONPATH:`pwd`/lib
echo "PYTHONPATH=$PYTHONPATH"
