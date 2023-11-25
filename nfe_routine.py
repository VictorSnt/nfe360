from nfeApi import download_nfe_pdf as get_pdfs
from nfeApi import download_nfe_xml as get_xmls
from nfeApi import get_nfe as get_nfes
from configuration.config import load_config
from database.DbConnect import DbConnection
from xml_manager import format_xml_to_wshop, xml_to_dict
from files_backup import backup_routine
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import asyncio
import json
import os


load_dotenv()
conf = load_config()
if not conf: input('Database Conigurations error')
db_conn = DbConnection(conf['HOST'], conf['PORT'], conf['DBNAME'], conf['USER'], conf['PASSWD'])
if not db_conn.connect(): input('Erro ao conectar no banco')
DOWNLOADS_FOLDER = Path(os.environ.get('DOWNLOADS_FOLDER', None))
CACHE_JSON = Path(os.environ.get('CACHE_JSON', None))

def run_rotine():
    
    any_new_data = False
    data_list = asyncio.run(get_nfes.reload_nfe())
    access_key_dict = {d.stem: str(d) for d in DOWNLOADS_FOLDER.iterdir() if d.name.endswith('.xml')}
    xml_files = [str(d) for d in DOWNLOADS_FOLDER.iterdir() if d.name.endswith('.xml')]
    format_xml_to_wshop(xml_files)
    if not xml_files:
        with open(CACHE_JSON, 'w') as json_cache_file:
            json.dump(data_list, json_cache_file, indent=4)
    
    else:
        xml_as_dicts = xml_to_dict(DOWNLOADS_FOLDER)
        xml_as_dicts.sort(key=lambda x: datetime.strptime(x['Data de Emiss\u00e3o: '], 
        '%d/%m/%Y %H:%M:%S'), reverse=True)
        
        for index, xml in enumerate(xml_as_dicts):
            xml_date = datetime.strptime(xml["Data de Emiss\u00e3o: "], '%d/%m/%Y %H:%M:%S')
            xml_string = xml_date.strftime('%Y-%m-%d')
            print(xml_string)
            query = f'''
                        SELECT * FROM wshop.documen
                        WHERE nrdocumento = '{xml['nfe']}'
                        AND dtreferencia BETWEEN '{xml_string}' AND CURRENT_DATE
                    '''
            response = db_conn.sqlquery(query)
            print(response)
            if not response: 
                xml_as_dicts[index]['alterdata'] = False 
            else:
                xml_as_dicts[index]['alterdata'] = True
        with open(CACHE_JSON, 'w') as json_cache_file:
            json.dump(xml_as_dicts, json_cache_file, indent=4)
    
    format_xml_to_wshop(xml_files)
    
    for nf in data_list:
            
            nfe_access_key = nf['access_key']

            if str(nfe_access_key).isnumeric() and not access_key_dict.get(nfe_access_key, False):
                success = asyncio.run(get_xmls.alternative_download_nf_xml(nfe_access_key, DOWNLOADS_FOLDER))
                while not success:
                    success = asyncio.run(get_xmls.alternative_download_nf_xml(nfe_access_key, DOWNLOADS_FOLDER))
                    if not success:
                      success = asyncio.run(get_xmls.download_nf_xml(nfe_access_key, DOWNLOADS_FOLDER))   
                print(f' Download of {nfe_access_key} is done')
                any_new_data = True
            else:
                print("already on downloads folder")
    
    if any_new_data:
        asyncio.run(get_pdfs.download_nfe_pdf((DOWNLOADS_FOLDER)))
        backup_routine()
    
    print('Routine done')


if __name__ == '__main__':
    run_rotine()
