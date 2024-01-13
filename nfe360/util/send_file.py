from io import BytesIO
from flask import Flask, send_file
from nfe360.models.nfe import Nfe
from pathlib import Path


def handler_file_type(filename: Path, wraped_nfe: list[Nfe]|list[None]) -> str:
    
    if not filename:
        raise ValueError("O Nome do arquivo requisitado não esta na request")
    
    if not wraped_nfe:
        raise ValueError("response deveria conter um instancia de Nfe")
            
    nfe = wraped_nfe[0]
    
    if filename.suffix == '.xml':
        xml_byteIo = BytesIO(nfe.xmlstring)
            
        return send_file(
            xml_byteIo, 
            as_attachment=True, 
            download_name=filename.name
        )
        
    else:
        pdf_byteIo = BytesIO(nfe.danfebinary)
        return send_file(pdf_byteIo, mimetype='application/pdf')

