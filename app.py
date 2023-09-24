from flask import Flask, render_template, send_file, request, redirect
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from xml_manager import xml_to_dict


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


@app.route('/search_data')
def get_searched_file():

    initial_filtered_date = (request.args.get('search_key', None))
    final_filtered_date = request.args.get('search_key2', None)
    if initial_filtered_date and final_filtered_date:
        
        initial_filtered_date = datetime.strptime(initial_filtered_date, '%Y-%m-%d')
        final_filtered_date = datetime.strptime(final_filtered_date, '%Y-%m-%d')

        all_xml_data = xml_to_dict(DOWNLOADS_FOLDER)
        
        filtered_xml_data = [
            xml_info for xml_info in all_xml_data
            if datetime.strptime(xml_info["Data de Emiss\u00e3o: "], '%d/%m/%Y') >= initial_filtered_date
            and datetime.strptime(xml_info["Data de Emiss\u00e3o: "], '%d/%m/%Y') <= final_filtered_date
            ]

        filtered_xml_data.sort(key=lambda x: x["Data de Emiss\u00e3o: "])

        return render_template('index.html', nfelist=filtered_xml_data)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

