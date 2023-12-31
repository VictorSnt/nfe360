import xmltodict
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta


def format_xml_to_standard(xml_dir: list):
    for xml_path in xml_dir:
        with open(xml_path, 'r', encoding='utf-8') as xml_file:
            xml_dict = xml_file.read()
        
        def modificar_dict(xml_string):
            root = ET.fromstring(xml_string)

            for infNFe in root.iter('{http://www.portalfiscal.inf.br/nfe}infNFe'):
                for det in infNFe.iter('{http://www.portalfiscal.inf.br/nfe}det'):
                    nItem = det.find('./{http://www.portalfiscal.inf.br/nfe}nItem')
                    if nItem is not None:
                        det.attrib['nItem'] = nItem.text
                        det.remove(nItem)

            return ET.tostring(root, encoding='utf-8').decode('utf-8')

        

        xml_modificado = modificar_dict(xml_dict)

        with open(xml_path, 'w', encoding='utf-8') as output_file:
            output_file.write(xml_modificado)

        


def xml_to_dict(downloads_folder):
    
    xml_info_list = []
    xml_files = [str(xml) for xml in downloads_folder.iterdir() if str(xml.name).endswith('.xml')]
    
    for file in xml_files:
        data = {}
        with open(file, 'r', encoding='utf-8') as xml:
            data_dict = xmltodict.parse(xml.read())

        
        emitent_info = data_dict['ns0:nfeProc']['ns0:NFe']['ns0:infNFe']['ns0:emit']
        nfe_info = data_dict['ns0:nfeProc']['ns0:protNFe']['ns0:infProt']
        payment_info = data_dict['ns0:nfeProc']['ns0:NFe']['ns0:infNFe']['ns0:pag']['ns0:detPag']
        if isinstance(payment_info, list):
            data["Valor Total da NF-e: "] = payment_info[0]['ns0:vPag']
        else:
            data["Valor Total da NF-e: "] = payment_info['ns0:vPag']
        data["Raz\u00e3o Social do Emitente:"] = emitent_info['ns0:xNome']
        data["CNPJ/CPF:"] = emitent_info['ns0:CNPJ'] 
        data["Data de Emiss\u00e3o: "] = datetime.fromisoformat(nfe_info['ns0:dhRecbto']).astimezone(timezone(timedelta(hours=-3)))
        data["Data de Emiss\u00e3o: "] = data["Data de Emiss\u00e3o: "].strftime('%d/%m/%Y %H:%M:%S')
        
        data['access_key'] = nfe_info['ns0:chNFe']
        data['nfe'] = data_dict['ns0:nfeProc']['ns0:NFe']['ns0:infNFe']['ns0:ide']['ns0:nNF']
        xml_info_list.append(data)
    
    return xml_info_list


