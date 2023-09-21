import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from download_nfe_xml import download_nf_xml
from bs4 import BeautifulSoup


async def reload_nfe():
    
    async with async_playwright() as p:
        browser = await p.firefox.launch_persistent_context(
            './profile',
            headless=True
        )
        
        
        
        page = await browser.new_page()
        await page.goto('https://www.nfe.fazenda.gov.br/portal/manifestacaoDestinatario.aspx?tipoConteudo=o9MkXc+hmKs=')
        
        # Insira aqui as ações que deseja realizar na página
        await page.wait_for_selector('#ctl00_ContentPlaceHolder1_rbtSemChave')
        await page.click('#ctl00_ContentPlaceHolder1_rbtSemChave')

        await page.wait_for_selector('#ctl00_ContentPlaceHolder1_btnPesquisar')
        await page.click('#ctl00_ContentPlaceHolder1_btnPesquisar')

        await page.wait_for_selector('#ctl00_ContentPlaceHolder1_gdvResultadoPesquisa')
        resultsTable = await page.query_selector('#ctl00_ContentPlaceHolder1_gdvResultadoPesquisa')
        
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
        link_elements = soup.findAll('a')
        data: dict = {}
        data_list: list = []
        
        for link in link_elements:
            for span_ in elements:
                texto_do_span = span_.text if span_.text else ''
                texto_fora_do_span = span_.find_next_sibling(text=True).strip() if span_.find_next_sibling() else ''
                
                if not texto_do_span == '':
                    data[texto_do_span] = texto_fora_do_span
                else:
                    data['access_key'] = str(link.text).strip() if link.text else None
                    data_list.append(data)
                    data = {}
                    break
        
        browser.close()
        downloads_folder = Path('downloads\\')
        access_key_list = [str(d.name) for d in downloads_folder.iterdir()]
        for nf in data_list:
            nfe_access_key = nf['access_key']
            if str(nfe_access_key).isnumeric() and all([nfe_access_key not in key for key in access_key_list]):
                await download_nf_xml(nfe_access_key)
                print(f' Download of {nfe_access_key} is done')
            else:
                print("already on downloads folder")
        
        
        return data_list
    

if __name__ == '__main__':
    def init_async():
        asyncio.run(reload_nfe())
    init_async()

