import os
import subprocess
from flask import Flask, render_template, request, send_file
from pdf2docx import parse

# Docker container ke andar files /app folder mein hoti hain
app = Flask(__name__, template_folder='/app/templates') 
UPLOAD_FOLDER = '/tmp'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/convert', methods=['POST'])
def Receive_file():
    user_file = request.files['user_file']
    saved_path = os.path.join(UPLOAD_FOLDER, user_file.filename)
    user_file.save(saved_path)
    
    # PDF to Word conversion (using pdf2docx)
    out_file = saved_path.replace(".pdf", ".docx")
    parse(saved_path, out_file)
    return send_file(out_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
