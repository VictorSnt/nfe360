from nfe360.database.queries import create_table_query, \
    nfes_by_status, all_inactive_nfes, all_valid_nfes, all_nfes

from contextlib import contextmanager
from typing import Any, Type
import sqlite3

from nfe360.util.search_logic import buscar_string
from nfe360.util.datetime import order_by_date
from nfe360.models.nfe import Nfe


class DbConnection:

    def __init__(self, database: str):
        self.database = database
        self.error = None
        self.conn = None
        self.cursor = None

    @contextmanager
    def connect(self) -> Type["DbConnection"]:
        try:
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
            self.cursor.execute(create_table_query)
            self.conn.commit()
            yield self  
        except sqlite3.Error as e:
            raise e
        finally:
            self.closeconnection()
            

    def sqlquery(
            self, 
            query: str, 
            argumensts: bool|tuple[Any]=False, 
            commit: bool=False) -> list[Nfe]|list[None]:

        if not self.cursor:
            raise sqlite3.Error("Você não esta conectado em nenhum banco")   
         
        try:
            if not argumensts:
                self.cursor.execute(query)
            
            else:
                self.cursor.execute(query, argumensts)
            
            if commit:
                return

            columns = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            results_list = [
                Nfe(**{column: value for column, value in zip(columns, row)})
                for row in rows]
            
            results_list = order_by_date(results_list)
            return results_list or []

        except sqlite3.Error as e:
            raise e


    def retrieve_all_valid_nfe(
            self, registered: str ='all', 
            search_key: str|bool = False

            ) -> list[Nfe]:
        """
        Retrieve NFEs based on different criteria.

        Parameters:
        - registration_status (str): Filter by registration status ('all', 'False', 'inactives' or 'True').
        - search_key (bool): If True, perform additional search based on a key.

        Returns:
        - list[Nfe]: List of NFEs matching the criteria.
        """
        try:
            if registered == 'all':
                retrieve_query = all_valid_nfes

            elif registered == 'inactives':
                retrieve_query = all_inactive_nfes

            else:      
                retrieve_query = nfes_by_status.format(f"'{registered}'")
                
            nfes = self.sqlquery(retrieve_query)
            
            if not nfes:    
                raise ValueError(
                    "Nenhuma nota fiscal registrada, \"routine\" esta em execução?")
                
            if search_key:
                nfes = order_by_date(buscar_string(nfes, search_key))
            
            return nfes 
        
        except sqlite3.Error as e:
            raise e

    def retrieve_all_nfe(self) -> list[Nfe]|list[None]:
        
        try:   
            nfes = self.sqlquery(all_nfes)
            return nfes if nfes else []
        
        except sqlite3.Error as e:
            raise e

    def closeconnection(self) -> None:

        try:
            self.cursor.close()
            self.conn.close()
            self.error = None
            
        except sqlite3.Error as e:
            raise e
            
