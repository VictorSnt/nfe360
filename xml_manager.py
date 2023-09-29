import xmltodict
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta


def format_xml_to_wshop(xml_dir):
    for xml_path in xml_dir:
        with open(xml_path, 'r', encoding='utf-8') as xml_file:
            xml_dict = xmltodict.parse(xml_file.read())    
        
        def modificar_dict(dicionario):
            
            if isinstance(dicionario, dict):
                for chave, valor in dicionario.items():
                    if isinstance(valor, dict):
                        modificar_dict(valor)
        
                    if chave == 'det':
                        if isinstance(valor, list):
                            nItem = valor[0].get('nItem')
                            if nItem is not None:
                                valor[0]['@nItem'] = nItem
                                del valor[0]['nItem']

                        else:
                            nItem = valor.get('nItem')
                            if nItem is not None:
                                valor['@nItem'] = nItem
                                del valor['nItem']

        modificar_dict(xml_dict)

        xml_modificado = xmltodict.unparse(xml_dict, pretty=True)

        with open(xml_path, 'w', encoding='utf-8') as output_file:
            output_file.write(xml_modificado)

        print(f'Todas as ocorrências da tag <det> em {xml_path} foram modificadas.')


def xml_to_dict(downloads_folder):
    
    xml_info_list = []
    xml_files = [str(xml.absolute()) for xml in downloads_folder.iterdir() if str(xml.name).endswith('.xml')]
    
    for file in xml_files:
        data = {}
        with open(file, 'r') as xml:
            xml_string = xml.read()

        data_dict = xmltodict.parse(xml_string)
        emitent_info = data_dict['nfeProc']['NFe']['infNFe']['emit']
        nfe_info = data_dict['nfeProc']['protNFe']['infProt']
        payment_info = data_dict['nfeProc']['NFe']['infNFe']['pag']['detPag']
        if isinstance(payment_info, list):
            data["Valor Total da NF-e: "] = payment_info[0]['vPag']
        else:
            data["Valor Total da NF-e: "] = payment_info['vPag']
        data["Raz\u00e3o Social do Emitente:"] = emitent_info['xNome']
        data["CNPJ/CPF:"] = emitent_info['CNPJ'] 
        data["Data de Emiss\u00e3o: "] = datetime.fromisoformat(nfe_info['dhRecbto']).astimezone(timezone(timedelta(hours=-3)))
        data["Data de Emiss\u00e3o: "] = data["Data de Emiss\u00e3o: "].strftime('%d/%m/%Y')
        data['access_key'] = nfe_info['chNFe']
        data['nfe'] = data['access_key'][25:34]
        xml_info_list.append(data)
    
    return xml_info_list


