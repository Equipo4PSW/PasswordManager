import os, os.path
from whoosh.index import create_in, open_dir, exists_in, IndexError
# from whoosh.qparser import QueryParser, FuzzyTermPlugin

class Db:

    # ===== Constructor =====
    def __init__(self):
        # Define DB Schema
        from .schemas import passwordSchema
        self.schema = passwordSchema

        # Define and open database.
        DBPATH = "data"

        try:
            if not os.path.exists(DBPATH):
                os.mkdir(DBPATH)

            if exists_in(DBPATH):
                self.index = open_dir(DBPATH)
            else:
                self.index = create_in(DBPATH, self.schema)

        except IndexError as error:
            print("No se pudo abrir el indice", error)

    # ===== Methods =====
    from .functions import addDb
