import json
import os
from datetime import datetime

METADATA_FILE = "metadata/indexed_files.json"


def get_indexed_files():
    if not os.path.exists(METADATA_FILE):
        return []

    try:
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_metadata(data):
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def is_already_indexed(filename):

    files = get_indexed_files()

    return any(doc["filename"] == filename for doc in files)


def add_indexed_file(filename, chunks):

    files = get_indexed_files()

    files.append({
        "filename": filename,
        "chunks": chunks,
        "uploaded_at": datetime.now().isoformat()
    })

    save_metadata(files)