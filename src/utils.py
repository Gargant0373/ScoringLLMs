import csv
from dataclasses import dataclass
import os
import json

@dataclass
class SampleEntry:
    id: str
    sample: str

# Append data to a CSV file
def append_to_csv(file_path, data):
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

# Write the header if the file is empty
def write_header_if_empty(file_path, header):
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

# Load lyrics from specified file
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

def load_sample(json_path):
    with open(json_path, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)

    return [SampleEntry(id=entry['id'], sample=entry['sample']) for entry in data]
