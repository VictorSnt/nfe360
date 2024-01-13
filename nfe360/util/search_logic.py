from nfe360.models.nfe import Nfe


def buscar_string(lista: list[Nfe], termo: str) -> list[Nfe]:
    
    resultados = []
    last_var = 8
    for instancia in lista:
        termo = termo.lower()
        atributes = list(vars(instancia).values())[:last_var]
        
        if any(termo in str(valor).lower() for valor in atributes):
            resultados.append(instancia)
    
    return resultados