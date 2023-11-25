import asyncio
from playwright.async_api import async_playwright, Download

async def download_nf_xml(access_key, download_folder):
    
    try:
        filename = access_key + '.xml'
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False
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

            await page.wait_for_selector('#chaveAcessoBusca')
            await page.click('#chaveAcessoBusca')
            await page.keyboard.insert_text(access_key)

            await page.wait_for_selector('a[onclick="searchNfe()"]')
            await page.click('a[onclick="searchNfe()"]')

            await page.wait_for_selector('a[onclick="downloadXml()"]')
            downloadPromise = page.wait_for_event('download')
            await page.click('a[onclick="downloadXml()"]')
            download = await downloadPromise
            await download.save_as(download_folder / filename )
         
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
