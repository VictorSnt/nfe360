from bs4 import BeautifulSoup


with open('./nfeTable.html', 'r', encoding='iso-8859-1') as html_file:
    htmlContent = html_file.read()  # Use read() to read the entire content
soup = BeautifulSoup(htmlContent, 'html.parser')

# Encontre o elemento div com a classe "tooltip"
elements = soup.findAll('span')
data: dict = {}
data_list: list = []
for span_ in elements:
    texto_do_span = span_.text if span_.text else ''
    texto_fora_do_span = span_.find_next_sibling(text=True).strip() if span_.find_next_sibling() else ''
    
    if not texto_do_span == '':
        data[texto_do_span] = texto_fora_do_span
    else:
        data_list.append(data)
        data = {}
# Acesse o texto fora do span usando .next_sibling
data_list2[0]
data_list[0]

new = [item == x for item in data_list[0].values() for x in data_list2[0].values ]