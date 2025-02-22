
# Scoring LLMs Paper Repository
Project built with DSPy for ratings Song Lyrics.

## Setup
Create and activate a virtual environment
```
cd this/project/path/
python -m venv .venv
. .venv/bin/activate
```
Then install all dependencies with
```
pip install -r requirements.txt
```
Run scripts from `src/` with
```
python src/{name of script}
```
For running ratings, you can find out the necessary parameters by doing
```
python src/ratings.py --help
```

**.env example configuration:**

    RESULTS_DIR=/home/user/ScoringLLMs/results
    LYRICS_PATH_IDS=/home/user/ScoringLLMs/data/ids.csv
    LYRICS_PATH_FULL=/home/user/ScoringLLMs/data/full.csv
    LOG_DIR=/home/adespan/user/logs
    PLOT_PATH=/home/adespan/user/plot
