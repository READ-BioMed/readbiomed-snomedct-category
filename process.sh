#!/bin/sh
cd /metamap/public_mm
./bin/skrmedpostctl start

cd /MCRI
python3 process.py