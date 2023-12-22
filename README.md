# NFe 360

[![Licença: MIT](https://img.shields.io/badge/Licença-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Status do Projeto: Em desenvolvimento :dash:

## Descrição

O NFe 360 é um projeto web desenvolvido em Flask, criado para o controle de notas fiscais em empresas de pequeno e médio porte que não possuem essa funcionalidade incorporada em seus sistemas principais. Este sistema cria um controle de nota fiscal a partir da data de instalação, baseando-se em web scraping com Playwright para obter os XMLs das NFes emitidas em nome da empresa que utiliza a aplicação.

## Sumário
- [Requisitos](#Requisitos)
- [Instalação](#instalação)
- [Updates](#Updates)

## Requisitos

- Certificado digital A1: É necessário possuir um certificado digital A1 válido da empresa para realizar o controle de notas fiscais.

## Instalação

1. **Clone o repositório e acesse o diretório:**
    ```bash
    git clone https://github.com/VictorSnt/nfe360/
    cd nfe360
    ```
2. **Crie uma venv e instale as dependencias**
   ```bash
   py -m venv venv
   pip install -r requirements.txt
   playwright install
   ```
3. **Executar o script `seed_db.py`:**

    Ao executar o script pela primeira vez, é necessário realizar a aceitação manual do certificado do site. Abra o script `seed_db.py` e siga as instruções para aceitar o certificado. Após essa etapa inicial, o navegador pode ser configurado para rodar em modo headless para execuções subsequentes.
    ```bash
    python seed_db.py
    ```

## Updates

- Este projeto está em desenvolvimento ativo. Algumas das futuras melhorias planejadas incluem:
  - migração para FlaskReastful.
  - Aprimoramento da interface do usuário com front em react.
  - E mais!.

  Fique atento para mais atualizações.

---

**Nota:** Este projeto está em constante evolução. Agradeço contribuições e feedback!

## Documentação

(em breve)

## Licença

Este projeto é licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).
