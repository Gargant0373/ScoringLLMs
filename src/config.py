import os
import csv
from dotenv import load_dotenv
import logging


def setup_logging(log_dir):
    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the base level to DEBUG to capture all messages

    # Create handlers
    file_handler = logging.FileHandler(os.path.join(log_dir, "llama3.log"))
    file_handler.setLevel(logging.DEBUG)  # Log all messages to the file

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Log only INFO and above to the console

    # Create formatters and add them to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def load_lyrics(csv_path_mxm_id_list, csv_path_all_lyrics):
    ids = []
    with open(csv_path_mxm_id_list, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)
        for row in reader:
            ids.append(row['mxm_id'])

    data = []
    with open(csv_path_all_lyrics, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)
        for row in reader:
            mxm_id = row['mxm_id']
            if mxm_id in ids:
                data.append({
                    "mxm_id": mxm_id,
                    "lyrics": row['lyrics_body'],
                })

    return data
