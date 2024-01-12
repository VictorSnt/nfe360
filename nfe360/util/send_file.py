from flask import Flask, send_file
from nfe360.models.nfe import Nfe
from pathlib import Path


def handler_file_type(app: Flask ,filename: Path, wraped_nfe: Nfe) -> str:
    
    if not filename:
        raise ValueError("O Nome do arquivo requisitado não esta na request")
    
    if not wraped_nfe:
        raise ValueError("response deveria conter um instancia de Nfe")
            
    nfe = wraped_nfe[0]
    
    if filename.suffix == '.xml':
        
        required_file = app.static_folder + 'temp.xml'  
        with open(required_file, 'wb') as file_res:
            file_res.write(nfe.xmlstring)
            
        return send_file(
            required_file, 
            as_attachment=True, 
            download_name=filename.name
        )
        
    else:
        required_file = app.static_folder + 'temp.pdf'
        with open(required_file, 'wb') as file_res:
            file_res.write(nfe.danfebinary)
        return send_file(required_file)