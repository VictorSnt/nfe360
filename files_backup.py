from pathlib import Path
from dotenv import load_dotenv
from os import environ
from shutil import copy2


def backup_routine():
    load_dotenv()
    DOWNLOADS_FOLDER = Path(environ.get('DOWNLOADS_FOLDER', None))
    BACKUP_FOLDER = Path(environ.get('BACKUP_FOLDER', None))

    if not DOWNLOADS_FOLDER.exists() or not BACKUP_FOLDER.exists():
        print('pasta n exite') # error handler

    for file in DOWNLOADS_FOLDER.iterdir():
        copy2(file, BACKUP_FOLDER / file.name)
        print(f"O backup de {file.name} foi concluido")
    print("todos os backups foram feitos ")

if __name__ == "__main__":
    backup_routine()