import asyncio
from playwright.async_api import async_playwright, Download

async def download_nf():
    
    ACESS_KEY = '31230971481709000102550010000232761559210097'
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False
        )
        page = await browser.new_page()
        await page.goto('https://meudanfe.com.br/')
        
        # Insira aqui as ações que deseja realizar na página
        await page.wait_for_selector('#chaveAcessoBusca')
        await page.click('#chaveAcessoBusca')
        await page.keyboard.insert_text(ACESS_KEY)

        await page.click('a[onclick="searchNfe()"]')
        async def handle_download(download: Download):    
            filename = './downloads/'+ACESS_KEY+'.xml'
            await download.save_as(filename)
        page.on("download", handle_download)
        
        await page.click('#downloadXml')
        async def handle_download(download: Download):    
            filename = './downloads/'+ACESS_KEY+'.pdf'
            await download.save_as(filename)
        page.on("download", handle_download)
        await page.click('#downloadDanfePdf')
        
        await asyncio.sleep(5)
        await page.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(download_nf())
