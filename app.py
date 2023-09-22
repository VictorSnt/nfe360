from flask import Flask, render_template, send_file, request
from pathlib import Path
from dotenv import load_dotenv
import json
import os


load_dotenv()
DOWNLOADS_FOLDER = Path(os.environ.get('DOWNLOADS_FOLDER', None))
CACHE_JSON = Path(os.environ.get('CACHE_JSON', None))

app = Flask(__name__)

@app.route('/')
def display_recent_nfes():
    with open(CACHE_JSON, 'r') as json_cache_file:
        data_list = json.load(json_cache_file)
    return render_template('index.html', nfelist=data_list)

@app.route('/download')
def download_xml_or_danfe():
    
    filename = request.args.get('filename', False)
    
    if filename:
    
        required_file: Path = DOWNLOADS_FOLDER / filename
        
        if required_file.exists():
            return send_file(required_file, as_attachment=True, download_name=filename)
         
    
    return "File not found"


if __name__ == '__main__':
    app.run(debug=True)

