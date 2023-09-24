import xmltodict
from datetime import datetime, timezone, timedelta






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
        xml_info_list.append(data)
    
    return xml_info_list

