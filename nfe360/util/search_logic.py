from nfe360.models.nfe import Nfe


def buscar_string(lista: list[Nfe], termo: str) -> list[Nfe]:
    resultados = []
    for instancia in lista:
        termo = termo.lower()
        atributes = list(vars(instancia).values())[0:8]
        
        if any(termo in str(valor).lower() for valor in atributes):
            resultados.append(instancia)
    
    return resultados