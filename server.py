from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import io
from app.encryption.encrypt import encrypt_file
from app.encryption.decrypt import decrypt_file
from app.utils.file_handler import save_file, get_uploaded_files
from app.utils.metadata import save_metadata, get_metadata

UPLOAD_FOLDER = 'uploads/encrypted'
DECRYPTED_FOLDER = 'uploads/decrypted'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/encrypted'

@app.route('/')
def index():
    files = get_uploaded_files(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return "No selected file", 400

    file_bytes = uploaded_file.read()
    filename = uploaded_file.filename

    encrypted_bytes, metadata = encrypt_file(file_bytes, filename)
    save_file(encrypted_bytes, filename + ".enc", app.config['UPLOAD_FOLDER'])
    save_metadata(filename, metadata)

    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    base_name = os.path.splitext(filename)[0]  # remove .enc
    metadata = get_metadata(base_name)
    if metadata is None:
        return f"Metadata for {filename} is missing or invalid.", 404

    with open(encrypted_path, 'rb') as f:
        encrypted_bytes = f.read()

    decrypted_bytes = decrypt_file(encrypted_bytes, metadata)

    return send_file(
        io.BytesIO(decrypted_bytes),
        download_name=base_name,
        as_attachment=True
    )

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    base_name = os.path.splitext(filename)[0]
    metadata_path = os.path.join("uploads", "metadata", base_name + ".json")

    messages = []

    if os.path.exists(encrypted_path):
        os.remove(encrypted_path)
        messages.append(f"🗑 Deleted encrypted file: {filename}")
    else:
        messages.append(f"⚠️ Encrypted file not found: {filename}")

    if os.path.exists(metadata_path):
        os.remove(metadata_path)
        messages.append(f"🗑 Deleted metadata file: {base_name}.json")
    else:
        messages.append(f"⚠️ Metadata file not found: {base_name}.json")

    for msg in messages:
        print(msg)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
