from nfe360.database.DbConnect import DbConnection


db = DbConnection('nfe360/database/nfe360.db')
db.connect()

db.sqlquery('UPDATE nfes SET isvalid = TRUE', commit=True)
db.conn.commit()