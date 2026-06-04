
import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from pdf2docx import parse
import convertapi

convertapi.api_secret = 'TtD9o7vIAQv48mKR4KUIF2Rl6uPDuebm'

app = Flask(__name__, template_folder="templates")

# Linux server ke liye secure temporary folder
UPLOAD_FOLDER = '/tmp'


def Pdf_to_Word(pdf_path):
    word_out = pdf_path.replace(".pdf", ".docx")
    parse(pdf_path, word_out)
    return word_out

def Word_to_Pdf(word_path):
    pdf_out = word_path.replace(".docx", ".pdf")
    # Yeh external tool file ko bina server par load dale convert karega
    convertapi.convert('pdf', {'File': word_path}, from_format='docx').save_files(UPLOAD_FOLDER)
    return pdf_out

@app.route('/')
def index():
    return redirect(url_for('Receive_file'))

@app.route('/convert', methods=['GET','POST'])
def Receive_file():
    if request.method == 'POST':
        if 'user_file' not in request.files:
            return "No file uploaded", 400
            
        user_file = request.files['user_file']

        if user_file.filename != '':
            saved_path = os.path.join(UPLOAD_FOLDER, user_file.filename)
            user_file.save(saved_path)

            converted_file = ""
            
            if saved_path.endswith('.pdf'):
                try:
                    converted_file = Pdf_to_Word(saved_path)
                except Exception as e:
                    return f"Conversion failed: {str(e)}", 500
                     
            elif saved_path.endswith('.docx'):
                try:
                    converted_file = Word_to_Pdf(saved_path)
                except Exception as e:
                    return f"Word to PDF Conversion failed. API Key check karein. Error: {str(e)}", 500
                
            if converted_file:
                filename_only = os.path.basename(converted_file)
                return render_template("index.html", file_to_download=filename_only)

    return render_template("index.html")

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
