from nfeApi import download_nfe_pdf as get_pdfs
from nfeApi import download_nfe_xml as get_xmls
from nfeApi import get_nfe as get_nfes
from xml_manager import format_xml_to_wshop
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import json
import os



load_dotenv()
DOWNLOADS_FOLDER = Path(os.environ.get('DOWNLOADS_FOLDER', None))
CACHE_JSON = Path(os.environ.get('CACHE_JSON', None))

def run_rotine():
    
    any_new_data = False
    data_list = asyncio.run(get_nfes.reload_nfe())
    
    with open(CACHE_JSON, 'w') as json_cache_file:
         json.dump(data_list, json_cache_file, indent=4)
    access_key_dict = {d.stem: str(d) for d in DOWNLOADS_FOLDER.iterdir() if d.name.endswith('.xml')}
    xml_files = [str(d) for d in DOWNLOADS_FOLDER.iterdir() if d.name.endswith('.xml')]
    
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
    print('Routine done')


if __name__ == '__main__':
    run_rotine()