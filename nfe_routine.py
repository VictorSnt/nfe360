from nfeApi import download_nfe_pdf as get_pdfs
from nfeApi import download_nfe_xml as get_xmls
from nfeApi import get_nfe as get_nfes
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import json
import os



load_dotenv()
DOWNLOADS_FOLDER = Path(os.environ.get('DOWNLOADS_FOLDER', None))
CACHE_JSON = Path(os.environ.get('CACHE_JSON', None))

def run_rotine():
    data_list = asyncio.run(get_nfes.reload_nfe())
    with open(CACHE_JSON, 'w') as json_cache_file:
         json.dump(data_list, json_cache_file, indent=4)
    access_key_list = [str(d.name) for d in DOWNLOADS_FOLDER.iterdir()]
    for nf in data_list:
            nfe_access_key = nf['access_key']
            if str(nfe_access_key).isnumeric() and all([nfe_access_key not in key for key in access_key_list]):
                asyncio.run(get_xmls.download_nf_xml(nfe_access_key, DOWNLOADS_FOLDER))
                print(f' Download of {nfe_access_key} is done')
            else:
                print("already on downloads folder")
    asyncio.run(get_pdfs.download_nfe_pdf((DOWNLOADS_FOLDER)))
    print('Routine done')


if __name__ == '__main__':
    run_rotine()