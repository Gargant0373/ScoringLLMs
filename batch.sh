#!/bin/bash
# Grid search for different models, sample types, and batch sizes

batch_size=3
# models=("llama3.1:8b" "qwen2.5:7b" "mistral" "gemma2:9b" "phi4" "mistral-small:24b")
models=("qwen2.5:7b" "gemma2:9b" "phi4")
sample_path="data/lyrics_tmp.json"
sample_types="lyrics"

for model in "${models[@]}"
do
    for i in $(seq 1 $batch_size)
    do
        python src/ratings.py -i $sample_path -t $sample_types --min 0 --max 10 $model
    done
done
        
