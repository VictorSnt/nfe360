from nfe360.database.DbConnect import DbConnection


def make_db_conection(database_path: str) -> DbConnection: 
            
            db = DbConnection(database_path)
            db.connect()

            if db.error: 
                raise db.error

            return db