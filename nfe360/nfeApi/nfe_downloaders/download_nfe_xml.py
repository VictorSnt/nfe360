import asyncio
from playwright.async_api import async_playwright, Download

async def download_nf_xml(access_key, download_folder):
    
    try:
        filename = access_key + '.xml'
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True
            )
            page = await browser.new_page()
            
            await page.goto('https://consultadanfe.com/')
            await page.wait_for_selector('#chave')
            await page.click('#chave')
            await page.keyboard.insert_text(access_key)
            await page.click('button[class="g-recaptcha"]')

            downloadPromise = page.wait_for_event('download')
            await page.click('a[onclick="if (!window.__cfRLUnblockHandlers) return false; return DownXML()"]')
            download = await downloadPromise
            await download.save_as(download_folder / filename )
            await asyncio.sleep(5)
            await page.close()
            await browser.close()
            return True
    
    except Exception as e:
        return False





async def alternative_download_nf_xml(access_key, download_folder):
    

    try:
        filename = access_key + '.xml'

        async with async_playwright() as p:
            browser = await p.firefox.launch(
                headless=True
            )
            page = await browser.new_page()

            await page.goto('https://meudanfe.com.br/')
            inputs_de_texto = await page.query_selector_all('input[type="text"]')
            if inputs_de_texto:
                primeiro_input = inputs_de_texto[0]
                await primeiro_input.type(access_key)
            try:
                await page.eval_on_selector('button:has-text("Buscar DANFE/XML")', 'button => button.click()')
                print("Botão clicado com sucesso.")
            except Exception as e:
                print(f"Erro ao clicar no botão: {e}")
            await asyncio.sleep(10)
            try:
                buttons = await page.query_selector_all('button')
                if buttons:
                    xml_button = buttons[2]
                    await xml_button.click()
            except Exception as e:
                print(f"Erro: {e}")
  
            downloadPromise = page.wait_for_event('download')  
            download = await downloadPromise
            await download.save_as(download_folder / filename )
            print('baixado')
            await asyncio.sleep(10)  

            await page.close()
            await browser.close()
            return True
    except Exception as e:
        print(f"Erro: {str(e)}")
        return False

if __name__ == '__main__':
    def init_async():
        asyncio.run(download_nf_xml())
    init_async()
