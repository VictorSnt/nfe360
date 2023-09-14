import asyncio
from bs4 import BeautifulSoup
from pyppeteer import launch
from pyppeteer.element_handle import ElementHandle

async def main():
    # Abre o navegador em modo headless=False para visualização
    browser = await launch(headless=False)
    page = await browser.newPage()
    while True:
        try:
            await page.goto('https://www.nfe.fazenda.gov.br/portal/manifestacaoDestinatario.aspx?tipoConteudo=o9MkXc+hmKs=')
            
            await page.waitForSelector('#ctl00_ContentPlaceHolder1_rbtSemChave')
            await page.click('#ctl00_ContentPlaceHolder1_rbtSemChave')

            await page.waitForSelector('#ctl00_ContentPlaceHolder1_btnPesquisar')
            await page.click('#ctl00_ContentPlaceHolder1_btnPesquisar')

            await page.waitForSelector('#ctl00_ContentPlaceHolder1_gdvResultadoPesquisa')
            
            resultsTable: ElementHandle = await page.querySelector('#ctl00_ContentPlaceHolder1_gdvResultadoPesquisa')
            if resultsTable:
                # Use page.evaluate para obter o conteúdo do elemento
                htmlContent = await page.evaluate('(resultsTable) => resultsTable.outerHTML', resultsTable)
                soup = BeautifulSoup(htmlContent, 'html.parser')

                # Encontre a tabela pela ID (ou por outros meios, dependendo da sua situação)
                table = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_gdvResultadoPesquisa'})
                table['class'] = ['custom-table']

                # Defina as classes para as células de cabeçalho
                header_cells = table.find_all('th')
                for header_cell in header_cells:
                    header_cell['class'] = ['custom-header-cell']
                    header_cell['style'] = 'background-color: #3498db; color: #fff;'  # Azul para o cabeçalho

                # Defina as classes para as células de dados
                data_cells = table.find_all('td')
                for data_cell in data_cells:
                    data_cell['class'] = ['custom-data-cell']
                    data_cell['style'] = 'background-color: #f2f2f2; color: #333;'  # Cinza para os dados


                # Converta a tabela de volta para uma string HTML
                styled_html = str(table)
                # Agora 'content' conterá o texto do elemento
                with open('nfeTable.html', 'w') as html:
                    html.write(styled_html)
            else:
                print("Elemento não encontrado")
            
            
            
            
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            
            await asyncio.sleep(10)

asyncio.get_event_loop().run_until_complete(main())
