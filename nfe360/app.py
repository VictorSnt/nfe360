from flask import Flask, render_template, request, redirect, url_for
import dotenv

from nfe360.database.queries import inaticvate_query, get_from_key
from nfe360.util.send_file import handler_file_type
from nfe360.util.database import make_db_conection
from nfe360.util.pagination import paginate

from datetime import datetime
from pathlib import Path
import sys
import os

app = Flask(__name__)

dotenv.load_dotenv()
app.static_folder = Path(os.environ.get('STATIC_FOLDER', None)).absolute()
app.template_folder = Path(os.environ.get('TEMPLATES_FOLDER', None)).absolute()
DOWNLOADS_FOLDER =  Path(os.environ.get('DOWNLOADS_FOLDER', None))
MODULES_PATH = os.environ.get('MODULES_PATH', None)
DATABASE = Path(os.environ.get('DATABASE', False))
sys.path.append(MODULES_PATH)


@app.route('/')
def display_recent_nfes() -> str:

    try:
        
        db_path = DATABASE
        db = make_db_conection(db_path)
        registered = request.args.get('isregistered', 'all')
        search_key = request.args.get('search_key', False)
        
        with db.connect():
            data_list = db.retrieve_all_valid_nfe(registered, search_key)
        
        page: int = request.args.get('page', 1, type=int)
        pagination, paginated_data_list = paginate(page, data_list)
        current_url = request.url
        return render_template(
            
            'index.html', 
            nfelist=paginated_data_list, 
            pagination=pagination,
            current_url=current_url
        )
    
    except Exception as e:
        return render_template('error.html', error=str(e))
        
@app.route('/download')
def download_xml_or_danfe():
    
    try:
        
        db_path = DATABASE
        db = make_db_conection(db_path)
        filename = Path(request.args.get('filename', False))
         
        with db.connect():
            wraped_nfe = db.sqlquery(get_from_key,(filename.stem,))
        
        response = handler_file_type(app, filename, wraped_nfe)
        
        return response
        
    except Exception as e:
        return render_template('error.html', error=str(e))
        
@app.route('/invalidar_nfe', methods=['POST'])
def deny_nfe():
    
    try:
        
        nfe_key = request.form.get('nfe_key', False)
        redirect_url = request.form.get('url', False)
        db_path = DATABASE
        db = make_db_conection(db_path)
        
        with db.connect():
            db.sqlquery(inaticvate_query, (nfe_key,), commit=True)
            db.conn.commit()

        return redirect(f"{redirect_url}")
    
    except Exception as e:
        return render_template('error.html', error=str(e))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5600)

