import os
from flask import Flask, render_template, request, send_file
from pdf2docx import parse

app = Flask(__name__, template_folder='templates')
# Hum `/tmp` ka use karenge kyunki wahi allowed hai
UPLOAD_FOLDER = '/tmp'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/convert', methods=['POST'])
def Receive_file():
    if 'user_file' not in request.files:
        return "No file part", 400
        
    user_file = request.files['user_file']
    # File ko tmp folder mein save karo
    saved_path = os.path.join(UPLOAD_FOLDER, user_file.filename)
    user_file.save(saved_path)
    
    # Output file ka path bhi tmp folder mein rakho
    out_file = os.path.join(UPLOAD_FOLDER, user_file.filename.replace(".pdf", ".docx"))
    
    try:
        # Conversion
        parse(saved_path, out_file)
        return send_file(out_file, as_attachment=True)
    except Exception as e:
        return f"Conversion Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
