#!/bin/sh
echo "Use gcloud command line program to initialize the current environment"
. setup_env.sh
gcloud auth login
gcloud config set project $PROJECT
