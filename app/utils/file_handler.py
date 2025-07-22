import os

def save_file(file_bytes, filename, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'wb') as f:
        f.write(file_bytes)
    return file_path

def get_uploaded_files(folder_path):
    if not os.path.exists(folder_path):
        return []
    return [f for f in os.listdir(folder_path) if f.endswith('.enc')]
