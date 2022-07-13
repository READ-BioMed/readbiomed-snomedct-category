#!/bin/sh
cd /metamap/public_mm
./bin/skrmedpostctl start

cd /MCRI/src
python3 process.py