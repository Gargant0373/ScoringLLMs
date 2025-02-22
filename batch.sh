#!/bin/sh

for i in $(seq 1 10)
do
    echo "Run $i"
    python src/ratings.py -i "data/lyrics_v1_pilot.json" -t "lyrics" --min 0 --max 10 qwen2.5:7b 
    python src/ratings.py -i "data/speeches_v1_pilot.json" -t "speeches" --min 0 --max 10 qwen2.5:7b 
done

for i in $(seq 1 10)
do
    echo "Run $i"
    python src/ratings.py -i "data/lyrics_v1_pilot.json" -t "lyrics" --min 0 --max 10 llama3.1:8b 
    python src/ratings.py -i "data/speeches_v1_pilot.json" -t "speeches" --min 0 --max 10 llama3.1:8b 
done
