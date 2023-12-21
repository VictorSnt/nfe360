from nfe360.database.DbConnect import DbConnection


db = DbConnection('nfe360/database/nfe360.db')
db.connect()

query = """
-- Antes de executar a atualização, recomenda-se fazer backup dos dados ou testar em um ambiente de teste.
-- A conversão pode falhar se os dados não estiverem no formato esperado.

-- Adiciona uma nova coluna datetime temporária
ALTER TABLE nfes ADD COLUMN date_temp DATETIME;

-- Atualiza os valores da nova coluna com base na conversão da coluna original
UPDATE nfes SET date_temp = datetime(date, 'localtime');

-- Remove a coluna original
ALTER TABLE nfes DROP COLUMN date;

-- Renomeia a nova coluna para o nome original
ALTER TABLE nfes RENAME COLUMN date_temp TO date;


"""
db.sqlquery(query=query, commit=True)
db.conn.commit()