import os
from flask import Flask, render_template, request, send_file
import cloudconvert

app = Flask(__name__)
# Yahan apni CloudConvert API Key daalo (Free mein mil jati hai)
cloudconvert.configure(api_key='YOUR_API_KEY_HERE')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/convert', methods=['POST'])
def convert_file():
    file = request.files['user_file']
    # File upload karo
    upload = cloudconvert.Uploads.upload(file.stream, filename=file.filename)
    
    # Job create karo
    job = cloudconvert.Jobs.create(payload={
        "tasks": {
            "import-file": {
                "operation": "import/upload"
            },
            "convert-file": {
                "operation": "convert",
                "input": "import-file",
                "output_format": request.form.get('target_format') # User select karega
            },
            "export-file": {
                "operation": "export/url",
                "input": "convert-file"
            }
        }
    })
    
    # Wait and Download
    job = cloudconvert.Jobs.wait(id=job.id)
    file_url = cloudconvert.Tasks.export(id=job.tasks[2].id).url
    
    return f'<a href="{file_url}">Download Converted File</a>'
