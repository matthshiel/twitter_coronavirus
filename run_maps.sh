#!/bin/sh

for file in '/data/Twitter dataset/geoTwitter20'*.zip; do
    nohup python3 src/map.py --input_path="$file" > "$(basename "$file").log" 2>&1 &
done
