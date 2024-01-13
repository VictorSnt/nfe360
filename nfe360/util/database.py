from nfe360.database.DbConnect import DbConnection


def make_db_connection(database_path: str) -> DbConnection: 
    db = DbConnection(database_path)
    return db
