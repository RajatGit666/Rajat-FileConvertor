import os
import subprocess
from flask import Flask, render_template, request, send_file
from pdf2docx import parse

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'

def Word_to_Pdf(word_path):
    pdf_out = word_path.replace(".docx", ".pdf")
    # LibreOffice command ka istemal (Direct conversion)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', UPLOAD_FOLDER, word_path])
    return pdf_out

@app.route('/convert', methods=['POST'])
def Receive_file():
    user_file = request.files['user_file']
    saved_path = os.path.join(UPLOAD_FOLDER, user_file.filename)
    user_file.save(saved_path)
    
    if saved_path.endswith('.pdf'):
        out = saved_path.replace(".pdf", ".docx")
        parse(saved_path, out)
    else:
        out = Word_to_Pdf(saved_path)
    return send_file(out, as_attachment=True)
