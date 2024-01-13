from nfe360.models.nfe import Nfe
from datetime import datetime


def parse_date_str(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')

def parse_str_date(date: datetime) -> str:
    return datetime.strftime(date, '%d/%m/%Y %H:%M:%S')

def order_by_date(iter: list[Nfe]) -> list[Nfe]:

    iter = [
        setattr(nf, 'date', parse_date_str(nf.date)) or nf 
            for nf in iter]
    
    iter = sorted(iter, key=lambda nf: nf.date, reverse=True)

    iter = [
        setattr(nf, 'date', parse_str_date(nf.date)) or nf 
            for nf in iter]
    
    return iter