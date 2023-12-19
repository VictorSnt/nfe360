from nfe360.database.DbConnect import DbConnection


db = DbConnection('nfe360/database/nfe360.db')
db.connect()

data = db.retrieve_all_nfe()
print(len(data))
