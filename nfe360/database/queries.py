create_table_query: str = """
    CREATE TABLE IF NOT EXISTS nfes (
    id INTEGER PRIMARY KEY,
    issuer VARCHAR(40) NOT NULL,
    cnpj VARCHAR(40) NOT NULL,
    date DATETIME NOT NULL,
    nftotal FLOAT NOT NULL,
    key VARCHAR(80) UNIQUE NOT NULL,
    nfenumber VARCHAR(40) NOT NULL,
    isvalid BOOLEAN NOT NULL,
    isregistered BOOLEAN NOT NULL,
    xmlstring BLOB NOT NULL,
    danfebinary BLOB NOT NULL
    );

"""

nfe_insert_query: str = """
                INSERT INTO nfes (
                    issuer, cnpj, date, nftotal, key, nfenumber, isvalid, isregistered, xmlstring, danfebinary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

nfe_deletion_query: str = """
                        DELETE FROM nfes
                        WHERE key = ?
                """

inaticvate_query = """
    UPDATE nfes
    SET isvalid = FALSE
    WHERE key = ?
    """

get_from_key = 'SELECT * FROM nfes WHERE key = ?'