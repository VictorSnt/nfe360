from nfe360.database.queries import create_table_query
from datetime import datetime
from nfe360.models.nfe import Nfe
import sqlite3

def order_by_date(iter):

    iter = [setattr(nf, 'date', datetime.strptime(nf.date, '%d/%m/%Y %H:%M:%S')) or nf 
             for nf in iter]
    iter = sorted(iter, key=lambda nf: nf.date, reverse=True)
    iter = [setattr(nf, 'date', datetime.strftime(nf.date, '%d/%m/%Y %H:%M:%S')) or nf 
             for nf in iter]
    return iter
class DbConnection:

    def __init__(self, database: str):
        self.database = database
        self.error = None
        self.conn = None
        self.cursor = None

    def connect(self) -> None:
        try:

            self.conn: sqlite3.Connection = sqlite3.connect(self.database)
            self.cursor: sqlite3.Cursor = self.conn.cursor()
            self.cursor.execute(create_table_query)
            self.conn.commit()
        
        except sqlite3.Error as e:
            self.error: sqlite3.Error = e
            

    def sqlquery(
            self, 
            query: str, 
            argumensts: bool|tuple[any]=False, 
            commit: bool=False) -> list[Nfe]|None:

        if not self.cursor:
            
            raise sqlite3.Error("Você não esta conectado em nenhum banco")   
        else:
            
            try:
                if not argumensts:
                
                    self.cursor.execute(query)
                
                else:
                
                    self.cursor.execute(query, argumensts)
                
                if commit:
                    return

                columns = [desc[0] for desc in self.cursor.description]
                rows = self.cursor.fetchall()
                results_list = [Nfe(**{column: value for column, value in zip(columns, row)}) for row in rows]
                results_list = order_by_date(results_list)
                return results_list

            except sqlite3.Error as e:
                self.error = e


    def retrieve_all_valid_nfe(self) -> list[Nfe]:
        
        try:
            
            retrieve_query = """
                SELECT *
                FROM nfes
                WHERE isvalid = TRUE
                ORDER BY date DESC;

            """ 
            nfes = self.sqlquery(retrieve_query)
            return nfes if nfes else []
        
        except sqlite3.Error as e:
            self.error = e

    def retrieve_all_nfe(self):
        
        try:
            
            retrieve_query = """
                SELECT *
                FROM nfes
                ORDER BY date DESC;

            """ 
            nfes = self.sqlquery(retrieve_query)
            return nfes if nfes else []
        
        except sqlite3.Error as e:
            self.error = e

    def closeconnection(self) -> bool:

        try:
            self.cursor.close()
            self.conn.close()
            self.error = None
            return True

        except sqlite3.Error as e:
            self.error = e
            return False
