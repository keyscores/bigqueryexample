#!/bin/sh
echo "Use gcloud command line program to initialize the current environment"
. setup_env.sh
gcloud auth login
gcloud config set project $PROJECT

echo "Install xlrd as a dependency into $PROJECT"
git clone git@github.com:python-excel/xlrd.git
mv xlrd/xlrd $PROJECT/
rm -rf xlrd

echo "Install Google APIs Client Library for Python"
pip install google-api-python-client -t keyscores

echo "Install requests"
pip install requests -t keyscores

echo "Install gflags"
pip install python-gflags -t keyscores
