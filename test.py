from nfe360.database.DbConnect import DbConnection


db = DbConnection('nfe360/database/nfe360.db')
db.connect()

response = db.retrieve_all_nfe()
print(len(response))