import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from pdf2docx import parse

app = Flask(__name__, template_folder="templates")

# Linux server par files save karne ka sabse safe temporary folder
UPLOAD_FOLDER = '/tmp'

def Pdf_to_Word(pdf_path):
    word_out = pdf_path.replace(".pdf", ".docx")
    parse(pdf_path, word_out)
    return word_out

@app.route('/')
def index():
    return redirect(url_for('Receive_file'))

@app.route('/convert', methods=['GET','POST'])
def Receive_file():
    if request.method == 'POST':
        # File aayi hai ya nahi, pehle check karo
        if 'user_file' not in request.files:
            return "No file uploaded", 400
            
        user_file = request.files['user_file']

        if user_file.filename != '':
            # File ko server ke secure /tmp folder mein save karo
            saved_path = os.path.join(UPLOAD_FOLDER, user_file.filename)
            user_file.save(saved_path)

            converted_file = ""
            
            if saved_path.endswith('.pdf'):
                try:
                    converted_file = Pdf_to_Word(saved_path)
                except Exception as e:
                    return f"Conversion failed: {str(e)}", 500
                     
            elif saved_path.endswith('.docx'):
                # Free Linux server par MS Word nahi hota, isiliye ise disable kiya hai
                return "Word to PDF is not supported on this server architecture.", 400
                
            if converted_file:
                # Sirf file ka naam frontend ko bhejo
                filename_only = os.path.basename(converted_file)
                return render_template("index.html", file_to_download=filename_only)

    return render_template("index.html")

@app.route('/download/<filename>')
def download_file(filename):
    # Download karte waqt wapas /tmp folder se file uthao
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
