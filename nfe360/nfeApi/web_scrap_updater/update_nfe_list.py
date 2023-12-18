import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def reload_nfe():
    
    async with async_playwright() as p:
        browser = await p.firefox.launch_persistent_context(
            'nfe360/nfeApi/web_scrap_updater/playwright_lib_browser/profile',
            headless=False
        )
        
        
        nfe_table = Path('nfeTable.html')
        page = await browser.new_page()
        await page.goto('https://www.nfe.fazenda.gov.br/portal/manifestacaoDestinatario.aspx?tipoConteudo=o9MkXc+hmKs=')
        
        
        await page.wait_for_selector('#ctl00_ContentPlaceHolder1_rbtSemChave')
        await page.click('#ctl00_ContentPlaceHolder1_rbtSemChave')

        await page.wait_for_selector('#ctl00_ContentPlaceHolder1_btnPesquisar')
        await page.click('#ctl00_ContentPlaceHolder1_btnPesquisar')

        await page.wait_for_selector('#ctl00_ContentPlaceHolder1_gdvResultadoPesquisa')
        resultsTable = await page.query_selector('#ctl00_ContentPlaceHolder1_gdvResultadoPesquisa')
        
       
        htmlContent = await page.evaluate('(resultsTable) => resultsTable.outerHTML', resultsTable)
        
        with open(nfe_table, 'w') as html:
            html.write(htmlContent)

        with open(nfe_table, 'r', encoding='iso-8859-1') as html_file:
            htmlContent = html_file.read()  
        soup = BeautifulSoup(htmlContent, 'html.parser')

       
        elements = soup.findAll('span')
        link_elements = soup.findAll('a')
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
        
        for link, data in zip(link_elements, data_list):
            data['access_key'] = str(link.text).strip() if link.text and str(link.text).strip().isnumeric() else None

        await browser.close()
        nfe_table.unlink()
        return data_list
     

if __name__ == '__main__':
    def init_async():
        asyncio.run(reload_nfe())
    init_async()

