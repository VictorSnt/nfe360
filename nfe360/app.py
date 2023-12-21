from flask import Flask, render_template, send_file, request, redirect
from flask_paginate import Pagination
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from nfe360.database.DbConnect import DbConnection
from nfe360.models.nfe import Nfe
from pathlib import Path

import dotenv
import json
import sys
import os


load_dotenv()
app = Flask(__name__)

dotenv.load_dotenv()
    
ITEMS_PER_PAGE = 5
MODULES_PATH = os.environ.get('MODULES_PATH', None)
DOWNLOADS_FOLDER =  Path(os.environ.get('DOWNLOADS_FOLDER', None))
DATABASE = Path(os.environ.get('DATABASE', False))
app.static_folder = Path(os.environ.get('STATIC_FOLDER', None)).absolute()
app.template_folder = Path(os.environ.get('TEMPLATES_FOLDER', None)).absolute()
sys.path.append(MODULES_PATH)





@app.route('/')
def display_recent_nfes():

    db = DbConnection(DATABASE)
    db.connect()
    if db.error: raise db.error

    data_list = db.retrieve_all_nfe()
    page = request.args.get('page', 1, type=int)
    
    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    paginated_data_list = data_list[start_idx:end_idx]
    total_pages = (
        len(data_list) // ITEMS_PER_PAGE + (len(data_list) % ITEMS_PER_PAGE > 0)
    )
    pagination = Pagination(
        page=page, total=len(data_list), 
        per_page=ITEMS_PER_PAGE, bs_version=4
    )
    print(pagination.info)
    return render_template('index.html', nfelist=paginated_data_list, arquivo_nao_encontrado=False, pagination=pagination)


@app.route('/download')
def download_xml_or_danfe():
    
    filename = request.args.get('filename', False)
    if filename:
    
        required_file = DOWNLOADS_FOLDER / filename
        if required_file.exists() and required_file.name.endswith('.xml'):
            return send_file(required_file, as_attachment=True, download_name=filename)
        elif required_file.exists():
            is_file_sended = send_file(required_file)
            return is_file_sended
        else:
            return render_template('index.html', arquivo_nao_encontrado=True)


@app.route('/invalidar_nfe')
def deny_nfe():
    
    nfe_key = request.form.get('nfe_key', False)
    
    if not CANCELEDS_JSON.exists() or not nfe_key:
        return 'Não ha cancelados para ser exibidos' if CANCELEDS_JSON is False else 'Não ha chave para cancelar'
    
    with open(CANCELEDS_JSON, 'r') as canceleds_json:
        canceleds_json_data = json.load(canceleds_json)
    
    canceleds_json_data['nfe_key'] = True

    with open(CANCELEDS_JSON, 'r') as canceleds_json:
        json.dump(canceleds_json_data, canceleds_json, indent=4)
    
    return redirect('/')

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
    app.run(host='0.0.0.0', port=5600)

