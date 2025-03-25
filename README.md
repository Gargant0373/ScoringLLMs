
# Scoring LLMs Paper Repository
Project built with DSPy for ratings Song Lyrics.

## Setup
Create and activate a virtual environment
```
cd this/project/path/
python -m venv .venv
source .venv/bin/activate
```
Then install all dependencies with
```
pip install -r requirements.txt
```
## Run
Run scripts from `src/` with
```
python src/{name of script}
```
For running the annotation script, you can do the following:
```
python src/ratings.py -i {sample_path} -t "lyrics" --min 0 --max 10 {model}
```
This will start annotating the lyrics in `sample_path` using a scale from 1 to 10 for each value.

To find out additional parameters for the annotation script, you can run
```
python src/ratings.py --help
```

Several configuration options have to be set in a `.env` file. These are:
```
RESULTS_DIR=/home/user/ScoringLLMs/results
LOG_DIR=/home/adespan/user/logs
DSP_CACHEBOOL=False
```
