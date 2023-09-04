import os, os.path
from whoosh.index import create_in, open_dir, exists_in, IndexError
from typing import List

from .searcherMenu import SearcherMenu

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
    from .functions import addDb, deleteDb, updateDb

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
