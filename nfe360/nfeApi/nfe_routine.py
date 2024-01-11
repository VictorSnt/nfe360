import sys
import os
import dotenv
import asyncio
import json
import os
from nfe360.database.DbConnectPostgres import DbConnectPostgres

from nfe360.nfeApi.nfe_downloaders import download_nfe_pdf as get_pdfs
from nfe360.nfeApi.nfe_downloaders import download_nfe_xml as get_xmls
from nfe360.nfeApi.web_scrap_updater import update_nfe_list as get_nfes
from collections import defaultdict
from nfe360.database.queries import nfe_insert_query
from nfe360.database.DbConnect import DbConnection
from nfe360.ext.xml_handler import xml_manager
from nfe360.models.nfe import Nfe
from pathlib import Path


def run_download_rotine(db: DbConnection, DOWNLOADS_FOLDER: Path):
   
    data_list = asyncio.run(get_nfes.reload_nfe())

    if db.error: raise db.error

    all_nfes: list[Nfe] = db.retrieve_all_nfe() 
    
    for nf in data_list:
            
            key = nf['access_key']
            
            if not any([nfe_data.key == key for nfe_data in all_nfes]):     
                success = asyncio.run(
                    get_xmls.alternative_download_nf_xml(
                        key, DOWNLOADS_FOLDER)
                    )
                while not success:
                    
                    success = asyncio.run(
                        get_xmls.alternative_download_nf_xml(
                            key, DOWNLOADS_FOLDER)
                        )
                    if not success:
                      success = asyncio.run(
                          get_xmls.download_nf_xml(key, DOWNLOADS_FOLDER)
                          )   
                print(f' Download of {key} is done')
                
            else:
                print("already on downloads folder")
    
    if DOWNLOADS_FOLDER.exists() and any(DOWNLOADS_FOLDER.iterdir()):
        asyncio.run(get_pdfs.download_nfe_pdf(DOWNLOADS_FOLDER))


def seed_database(db: DbConnection, DOWNLOADS_FOLDER: Path) -> None:

    if db.error: raise db.error
    if not DOWNLOADS_FOLDER.exists() or not any(DOWNLOADS_FOLDER.iterdir()): return
    
    files: defaultdict[str:list[Path]] = defaultdict(list)
    file_extensions: list[str] = ['.xml', '.pdf']
    
    for file in DOWNLOADS_FOLDER.iterdir():
            if file.exists() and file.suffix in file_extensions:
                    files[file.stem].append(file)
    
    xml_index: int = 1
    xml_files: list[Path] = [
         
         file_list[xml_index] for file_list in files.values() 
         if len(file_list) > 1
        ]
    xml_manager.format_xml_to_standard(xml_dir=xml_files)
    xml_as_dicts: [list[dict]] = xml_manager.xml_to_dict(DOWNLOADS_FOLDER)

    for xml_dict in xml_as_dicts:
        
        key: str = xml_dict["access_key"]
        exact_file_quant: int = 2
        xml_n_danfe: list[Path]|list[None] = files.get(key, [])
        
        if len(xml_n_danfe) != exact_file_quant: raise Exception(
            f'pdf or xml missing\n key:{key}')
        pdf_path, xml_path = xml_n_danfe
        
        with open(xml_path, "rb") as xml, open(pdf_path, "rb") as pdf:
            xml_binary_data: bytes = xml.read()
            pdf_binary_data: bytes = pdf.read()
        
        arguments = (
            
            xml_dict["Raz\u00e3o Social do Emitente:"], 
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
    db.conn.commit()
    for d in DOWNLOADS_FOLDER.iterdir():
        d.unlink()
    
    
def main(only_seed=False):
     
    dotenv.load_dotenv()
    
    MODULES_PATH = os.environ.get('MODULES_PATH', None)
    DOWNLOADS_FOLDER =  Path(os.environ.get('DOWNLOADS_FOLDER', None))
    DATABASE = Path(os.environ.get('DATABASE', False))
    sys.path.append(MODULES_PATH)

    db = DbConnection(DATABASE)
    db.connect()

    if only_seed: 
        seed_database(db=db, DOWNLOADS_FOLDER=DOWNLOADS_FOLDER) 
        return
    
    run_download_rotine(db=db, DOWNLOADS_FOLDER=DOWNLOADS_FOLDER)
    seed_database(db=db, DOWNLOADS_FOLDER=DOWNLOADS_FOLDER)
    db_alterdata = DbConnectPostgres(
            os.environ['HOST'],
            os.environ['PORT'], 
            os.environ['DBNAME'], 
            os.environ['USER'], 
            os.environ['PASSWD']
        )
        
    if not db_alterdata.connect(): 
        input('Erro ao conectar no banco')
    
    nfes: list[Nfe] = db.retrieve_all_nfe()
    for nf in nfes:
        print("peguei as nfes")
        query = f'''
            SELECT iddocumento FROM wshop.documen
            WHERE nrdocumento = '{nf.nfenumber}'
            AND dtreferencia BETWEEN '{nf.date}' AND CURRENT_DATE
        '''
        response = db_alterdata.sqlquery(query)
        
        if response:
            db.sqlquery(
                f"UPDATE nfes SET isregistered = TRUE WHERE key = ?",
                (nf.key,),
                commit=True)
            db.conn.commit()
            print(db.error)


if __name__ == '__main__': 
    main()
