import os
import json
from datetime import datetime

METADATA_FOLDER = 'uploads/metadata'

def save_metadata(original_filename, metadata):
    os.makedirs(METADATA_FOLDER, exist_ok=True)
    metadata_path = os.path.join(METADATA_FOLDER, original_filename + '.json')
    metadata['original_filename'] = original_filename
    metadata['uploaded_at'] = datetime.now().isoformat()

    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)

def get_metadata(filename_with_ext):
    metadata_path = os.path.join(METADATA_FOLDER, filename_with_ext + '.json')
    if not os.path.exists(metadata_path):
        return None
    with open(metadata_path, 'r') as f:
        return json.load(f)
