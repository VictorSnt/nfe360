import asyncio
import zipfile
from pathlib import Path
from playwright.async_api import async_playwright



async def download_nfe_pdf():
    
    async with async_playwright() as p:
        browser = await p.firefox.launch_persistent_context(
            './profile',
            headless=False
        )
        
        
        
        page = await browser.new_page()
        await page.goto('https://www.fsist.com.br/converter-xml-nfe-para-danfe')

        await page.wait_for_selector('#arquivolab')
        file_input = page.locator('#arquivolab')
        downloads_folder = Path('downloads\\')
        xml_paths = [str(d.absolute()) for d in downloads_folder.iterdir() if str(d.absolute()).endswith('.xml')]
        await file_input.set_input_files(xml_paths)
        
        await page.click('td[style="width: 130px;"]')
        async def handle_download(download):    
            filename = 'downloads\\' + 'danfespack.zip'
            await download.save_as(filename)
        page.on("download", handle_download)
        await page.click('#msgsim')
        await page.click('#butlink')
        await asyncio.sleep(5)
        await page.close()
        await browser.close()
        
        zip_file_path = 'downloads\\' + 'danfespack.zip'
        destination_folder = 'downloads\\'
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
        Path(zip_file_path).unlink()
        Path('downloads/_JUNTO.pdf').unlink()

if __name__ == '__main__':
    asyncio.run(download_nfe_pdf())