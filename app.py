from flask import Flask, render_template, request,redirect,url_for,send_file
from pdf2docx import parse
from docx2pdf import convert

def Pdf_to_Word(pdf_in):
        word_out= pdf_in.replace(".pdf",".docx")
        parse(pdf_in,word_out)
        return word_out

def Word_to_Pdf(word_in):
      pdf_out=word_in.replace(".docx",".pdf")
      convert(word_in,pdf_out)
      return pdf_out


app=Flask(__name__,template_folder="templates")

@app.route('/')
def index():
    return redirect(url_for('Receive_file'))

@app.route('/convert', methods=['GET','POST'])
def Receive_file():
    if request.method == 'POST':
        New_file_aii = request.files['user_file']

        if New_file_aii.filename != '':
            saved_path = New_file_aii.filename
            New_file_aii.save(saved_path)

            converted_file=""
            
            if saved_path.endswith('.pdf'):
                 converted_file=Pdf_to_Word(saved_path)
                 
            
            elif saved_path.endswith('.docx'):
                 converted_file=Word_to_Pdf(saved_path)     
                 
            return render_template("index.html", file_to_download=converted_file)


    return render_template("index.html")

@app.route('/download/<filename>')
def download_file(filename):
     return send_file(filename,as_attachment=True)

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000) 
