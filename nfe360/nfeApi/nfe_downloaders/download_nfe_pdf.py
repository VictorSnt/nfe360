import asyncio
import zipfile
from pathlib import Path
from playwright.async_api import async_playwright



async def download_nfe_pdf(downloads_folder):
    
    async with async_playwright() as p:
        browser = await p.firefox.launch_persistent_context(
            'nfe360/nfeApi/web_scrap_updater/playwright_lib_browser/profile',
            headless=False
        )
        
       
        download_file_name = 'danfespack.zip'
        default_fsist_pdf_file = '_JUNTO.pdf'
        page = await browser.new_page()
        xml_paths = [str(d.absolute()) for d in downloads_folder.iterdir() if str(d.absolute()).endswith('.xml')]

        await page.goto('https://www.fsist.com.br/converter-xml-nfe-para-danfe')

        await page.wait_for_selector('#arquivolab')
        file_input = page.locator('#arquivolab')
        
        await file_input.set_input_files(xml_paths[-100:])
        
        await page.click('td[style="width: 130px;"]')
        async def handle_download(download):  
            filename = downloads_folder / download_file_name
            await download.save_as(filename)
        page.on("download", handle_download)
        await page.click('#msgsim')
        await page.click('#butlink')
        await asyncio.sleep(5)
        await page.close()
        await browser.close()
        
        zip_file_path = downloads_folder / download_file_name
        destination_folder = downloads_folder
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
        Path(zip_file_path).unlink()
        Path(downloads_folder / default_fsist_pdf_file).unlink()

if __name__ == '__main__':
    def init_async():
        asyncio.run(download_nfe_pdf())
    init_async() 