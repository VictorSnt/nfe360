from pathlib import Path
from xml_manager import xml_to_dict

def record_checkup(file_path: str):
    
    construfacil_checkin_nf_path: Path = Path('..\\Cosntrufacil_CheckUp\\checkUp\\blueprints\static\\nfe_to_check\\')
    xml_path: Path = Path('static\\downloads')
    xml_list = xml_to_dict(xml_path)
    checkin_nfe_list = {str(file.stem): file.absolute() for file in construfacil_checkin_nf_path.iterdir()}
    xml_nfe_list = {
        str(file.stem): file.absolute() for file in construfacil_checkin_nf_path.iterdir() 
        if str(file.name).endswith('.xml')
    }
    print(checkin_nfe_list)

record_checkup('s')