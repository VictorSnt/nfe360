from nfe360.database.DbConnect import DbConnection
from nfe360.database.queries import nfe_insert_query
from nfe360.ext.xml_handler import xml_manager
from collections import defaultdict
from nfe360.models.nfe import Nfe
from dotenv import load_dotenv
from pathlib import Path



import sys
import os


def seed_database() -> None:
    
    load_dotenv()
        
    MODULES_PATH: str = os.environ.get('MODULES_PATH', None)
    DOWNLOADS_FOLDER = Path(os.environ.get('DOWNLOADS_FOLDER', None))
    DATABASE = Path(os.environ.get('DATABASE', False))
    sys.path.append(MODULES_PATH)
    db = DbConnection(DATABASE)
    db.connect()

    if db.error: raise db.error
    if not DOWNLOADS_FOLDER.exists() or not any(DOWNLOADS_FOLDER.iterdir()): return
    
    files: defaultdict[str:list[Path]] = defaultdict(list)
    file_extensions: list[str] = ['.xml', '.pdf']
    
    for file in DOWNLOADS_FOLDER.iterdir():
            if file.exists() and file.suffix in file_extensions:
                    files[file.stem].append(file)

    xml_index: int = 1
    xml_files: list[Path] = [file_list[xml_index] for file_list in files.values()]
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

    

    data: list[Nfe] = db.sqlquery('select * from nfes')
    print(len(data))

if __name__ == '__main__':
        seed_database()