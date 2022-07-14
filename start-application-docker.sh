#!/usr/bin/env bash
if [ -z "$1" ] || [ -z "$2" ]
  then
    echo "No arguments supplied"
    echo "Enter one directory RFV input and one directory for the ouput"
    echo "For example: bash start-application-docker.sh /data/RFV /data/output"
else
  export INPUT_DIR=$1 #RFV Directory
  export OUTPUT_DIR=$2 #OUTPUT Directory
  docker run --network rfv_ontoserver --name rfv_process -t -d -v $INPUT_DIR:/MCRI/input/ -v $OUTPUT_DIR:/MCRI/output readbiomed/mcri_rfv_matrix
fi