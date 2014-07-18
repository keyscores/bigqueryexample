#!/bin/bash

DEV=1

while getopts "ph" option
do
    case "${option}" in
        p)
            echo "Upload a file to the production server's bucket"
            DEV=0
            ;;
        h)
            echo "-p to upload a file to the production server http://kinetic-physics-644.appspot.com"
            ;;
        *)
            echo "Usage: $0 [-p]"
            echo "Without -p, the file will default to upload onto http://localhost:8000"
            ;;
    esac
done

shift $((OPTIND-1))

if [[ $DEV -gt 0 ]]; then
    echo "Upload $1 to $SERVER/upload"
    curl -i -X "POST" \
        -H "X-Keyscores-Filename:$1" \
        -H "X-Keyscores-Bucket-Name:keyscores_test" \
        -H "Content-Type:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
        -T $1 $SERVER/upload
else
    SERVER=http://kinetic-physics-644.appspot.com
    echo "Upload $1 to $SERVER/upload"
    curl -i -X "POST" \
        -H "X-Keyscores-Filename:$1" \
        -H "X-Keyscores-Bucket-Name:keyscores_test" \
        -H "Content-Type:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
        -T $1 $SERVER/upload
fi
