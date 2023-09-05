import os
from whoosh.index import create_in, open_dir, exists_in, IndexError
from typing import List

# from globalVariables import DB_PASSWORD_PATH, DB_MASTER_PATH
from .globalVariables import DB_PASSWORD_PATH, DB_MASTER_PATH

from .searcherMenu import SearcherMenu

class Db:

    # ===== Constructor =====
    def __init__(self):
        # Define DB Schema
        from .schemas import passwordSchema, masterSchema
        self.schema = passwordSchema
        self.masterSchema = masterSchema

        # --- Define and open database. ---

        # Try open index for passwords
        try:
            os.makedirs(DB_PASSWORD_PATH, exist_ok=True)

            if exists_in(DB_PASSWORD_PATH):
                self.index = open_dir(DB_PASSWORD_PATH)
            else:
                self.index = create_in(DB_PASSWORD_PATH, self.schema)

        except IndexError as error:
            print("No se pudo abrir el indice de las contraseñas", error)

        # Try open index for master password
        try:
            os.makedirs(DB_MASTER_PATH, exist_ok=True)

            if exists_in(DB_MASTER_PATH):
                self.masterIndex = open_dir(DB_MASTER_PATH)
            else:
                self.masterIndex = create_in(DB_MASTER_PATH, self.masterSchema)

        except IndexError as error:
            print("No se pudo abrir el indice de las contraseñas maestras", error)

    # ===== Methods =====
    from .functions.master import addMasterDb, verifyHandler, checkTime
    from .functions.password import addDb, deleteDb, updateDb

    from .passwords import generate_key

    def searchPassword(self, word:str) -> dict:
        # Display searcher engine
        searcher = SearcherMenu(self.index, word)
        result = searcher.run()
        return result

    def getPasswords(self, tagsList:List[str]):
        # Gets a string of tags separated by commas.
        tags = ",".join(tagsList)

        # Search passwords with tags and display
        searcher = SearcherMenu(self.index, tags)
        searcher.getPasswords(tags)

    def generateKey(self):
        from .passwords import generate_key
        generate_key()

    def passwordGenerator(self, size:int, a:bool, A:bool, n:bool, sym:str) -> str:
        from .passwords import generate_pasword

        return generate_pasword(size, a, A, n, sym)
