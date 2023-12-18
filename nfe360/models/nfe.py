from datetime import datetime
 
class Nfe:
    def __init__(self, id, issuer, cnpj, date, nftotal, key, nfenumber, isvalid, isregistered, xmlstring, danfebinary):
        self.id: int = id
        self.issuer: str = issuer
        self.cnpj: str = cnpj
        self.date: datetime = date
        self.nftotal: float = nftotal
        self.key: str = key
        self.nfenumber: str = nfenumber
        self.isvalid: bool = isvalid
        self.isregistered: bool = isregistered
        self.xmlstring: bytes = xmlstring
        self.danfebinary: bytes = danfebinary
    
    def __repr__(self) -> str:
        return f'{self.issuer} N°:{self.nfenumber}'