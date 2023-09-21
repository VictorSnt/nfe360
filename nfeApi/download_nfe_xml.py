import asyncio
from playwright.async_api import async_playwright, Download

async def download_nf_xml(access_key):
    
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True
        )
        page = await browser.new_page()
        await page.goto('https://consultadanfe.com/')
        
        # Insira aqui as ações que deseja realizar na página
        await page.wait_for_selector('#chave')
        await page.click('#chave')
        await page.keyboard.insert_text(access_key)

        await page.click('button[class="g-recaptcha"]')
        async def handle_download(download: Download):    
            filename = 'downloads\\' + access_key + '.xml'
            await download.save_as(filename)
        page.on("download", handle_download)
        await page.click('a[onclick="if (!window.__cfRLUnblockHandlers) return false; return DownXML()"]', timeout=10000000)
        
        await asyncio.sleep(5)
        await page.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(download_nf_xml())
