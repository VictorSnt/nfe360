import asyncio
from bs4 import BeautifulSoup
from pyppeteer import launch
from pyppeteer.element_handle import ElementHandle

async def main():
    # Abre o navegador em modo headless=False para visualização
    browser = await launch(headless=False)
    page = await browser.newPage()
    data_list2 = False
    while True:
        
        await page.goto('https://www.nfe.fazenda.gov.br/portal/manifestacaoDestinatario.aspx?tipoConteudo=o9MkXc+hmKs=')
        
        await page.waitForSelector('#ctl00_ContentPlaceHolder1_rbtSemChave')
        await page.click('#ctl00_ContentPlaceHolder1_rbtSemChave')

        await page.waitForSelector('#ctl00_ContentPlaceHolder1_btnPesquisar')
        await page.click('#ctl00_ContentPlaceHolder1_btnPesquisar')

        await page.waitForSelector('#ctl00_ContentPlaceHolder1_gdvResultadoPesquisa')
        
        resultsTable: ElementHandle = await page.querySelector('#ctl00_ContentPlaceHolder1_gdvResultadoPesquisa')
        
        # Use page.evaluate para obter o conteúdo do elemento
        htmlContent = await page.evaluate('(resultsTable) => resultsTable.outerHTML', resultsTable)
        # Agora 'content' conterá o texto do elemento
        with open('nfeTable.html', 'w') as html:
            html.write(htmlContent)

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
        if not data_list2:
            data_list2 = data_list
            data_list[0]['id'] = 'test'
        

        new = not(all([x in data_list[0] for x in data_list2[0]]))
        if new:
            data_list[0].pop('id')
            #send json data to web app
            print('new data')
        else:
            print('nothing new')
            
            
            
            
        
            
        await asyncio.sleep(10)

asyncio.get_event_loop().run_until_complete(main())
