from nfe360.database.DbConnect import DbConnection
from nfe360.models.nfe import Nfe
from nfe360.nfeApi.nfe_routine import run_rotine
from nfe360.database.queries import nfe_deletion_query


# db = DbConnection('nfe360/database/nfe360.db')
# db.connect()

# data = db.retrieve_all_nfe()
# data_id = tuple([nf.key for nf in data if nf.key == '31231217359233000188550010200643011270005958'])
# input(data_id)
# db.sqlquery(query=nfe_deletion_query, argumensts=data_id, commit=True)
# if db.error: raise db.error
# db.conn.commit()
run_rotine()