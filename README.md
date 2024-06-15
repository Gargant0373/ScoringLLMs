
# Scoring LLMs Paper Repository
Project built with DSPy for ratings Song Lyrics.

## Setup
Make sure a version of Conda is installed. Then
```
conda create -n scoring-llms python=3.9
conda activate scoring-llms
```
```
pip install -r requirements.txt
```
Run scripts from `src/` with
```
python src/{name of script}
```

**.env example configuration:**

    RESULTS_DIR=/home/user/ScoringLLMs/results
    LYRICS_PATH_IDS=/home/user/ScoringLLMs/data/ids.csv
    LYRICS_PATH_FULL=/home/user/ScoringLLMs/data/full.csv
    LOG_DIR=/home/adespan/user/logs
    PLOT_PATH=/home/adespan/user/plot
