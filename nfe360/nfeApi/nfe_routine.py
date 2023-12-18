import sys
import os
import dotenv
import asyncio
import json
import os

from nfe360.nfeApi.nfe_downloaders import download_nfe_pdf as get_pdfs
from nfe360.nfeApi.nfe_downloaders import download_nfe_xml as get_xmls
from nfe360.nfeApi.web_scrap_updater import update_nfe_list as get_nfes
from nfe360.database.queries import nfe_insert_query
from nfe360.database.DbConnect import DbConnection
from nfe360.ext.xml_handler import xml_manager
from nfe360.models.nfe import Nfe
from  pathlib import Path


def run_rotine():

    dotenv.load_dotenv()
    
    MODULES_PATH = os.environ.get('MODULES_PATH', None)
    DOWNLOADS_FOLDER =  Path(os.environ.get('DOWNLOADS_FOLDER', None))
    CACHE_JSON =  Path(os.environ.get('CACHE_JSON', None))
    DATABASE = Path(os.environ.get('DATABASE', False))
    sys.path.append(MODULES_PATH)
    
   
    data_list = asyncio.run(get_nfes.reload_nfe())

    db = DbConnection(DATABASE)
    db.connect()
    if db.error: raise db.error

    all_nfes: list[Nfe] = db.retrieve_all_nfe() 
    
    for nf in data_list:
            
            nfe_access_key = nf['access_key']
            
            if not any([nfe_data.key == nfe_access_key for nfe_data in all_nfes]):     
                success = asyncio.run(
                    get_xmls.alternative_download_nf_xml(nfe_access_key, DOWNLOADS_FOLDER)
                    )
                while not success:
                    
                    success = asyncio.run(
                        get_xmls.alternative_download_nf_xml(nfe_access_key, DOWNLOADS_FOLDER)
                        )
                    if not success:
                      success = asyncio.run(
                          get_xmls.download_nf_xml(nfe_access_key, DOWNLOADS_FOLDER)
                          )   
                print(f' Download of {nfe_access_key} is done')
                
            else:
                print("already on downloads folder")
    
     
    xml_file_dict = {
    d.stem: str(d) for d in DOWNLOADS_FOLDER.iterdir() 
        if d.exists() and d.name.endswith('.xml')
    }

    pdf_file_dict = {
        d.stem: str(d) for d in DOWNLOADS_FOLDER.iterdir() 
            if d.exists() and d.name.endswith('.pdf')
        }
    
    if xml_file_dict:
        asyncio.run(get_pdfs.download_nfe_pdf((DOWNLOADS_FOLDER)))
        xml_manager.format_xml_to_standard(xml_dir=xml_file_dict)
        xml_as_dicts = xml_manager.xml_to_dict(DOWNLOADS_FOLDER)
        
        for xml_dict in xml_as_dicts:

            xml_path = xml_file_dict.get(xml_dict["access_key"], False)
            pdf_path = pdf_file_dict.get(xml_dict["access_key"], False)
            
            if not xml_path or not pdf_path: continue
            
            with open(xml_path, "rb") as xml, open(pdf_path, "rb") as pdf:
                xml_binary_data = xml.read()
                pdf_binary_data = pdf.read()
            
            arguments = (xml_dict["Raz\u00e3o Social do Emitente:"], 
            xml_dict['CNPJ/CPF:'], 
            xml_dict["Data de Emiss\u00e3o: "], 
            xml_dict["Valor Total da NF-e: "],
            xml_dict["access_key"],
            xml_dict["nfe"],
            True,
            False,
            xml_binary_data,
            pdf_binary_data,
            )
            db.sqlquery(query=nfe_insert_query, argumensts=arguments, commit=True)
    
    else:
        print('everything was already updated')
        return
    db.conn.commit()
    
    # for d in DOWNLOADS_FOLDER.iterdir():
    #     d.unlink()

if __name__ == '__main__':
    run_rotine()
