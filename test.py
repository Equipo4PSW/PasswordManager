from whoosh.qparser import QueryParser, FuzzyTermPlugin
from backend import Db, SearcherMenu

dbHandler = Db()

# TODO: Ojo si se spamea mucho el codigo, deja de agregar cosas, se podria testear cuando se complete el buscador.
# dbHandler.addDb("abc123", ['Netflix', 'suegra'])
# dbHandler.addDb("abc123", ['Netflix', 'yo'])
# dbHandler.addDb("abc12345", ['Facebook', 'suegra'])
# dbHandler.addDb("abc12345", ['Facebook', 'yo'])
# dbHandler.addDb("abcdb12345", ['mi contra del face'])
# dbHandler.addDb("abcdb12345", ['mi contra del yutu'])
# dbHandler.addDb("hola123", ['Borrar'])
# dbHandler.addDb("aabbc", ['Change password'])
# dbHandler.addDb("aabb", ['change'])

# writer = db.writerDB
# writer.add_document(id=str(uuid.uuid4()), password='abc123', tags="netflix, suegra")
# writer.add_document(id=str(uuid.uuid4()), password='abc123344', tags="face, suegra")
# writer.add_document(id=str(uuid.uuid4()), password='abcdas123', tags="youtube, suegra")
# writer.add_document(id=str(uuid.uuid4()), password='aaaaa123', tags="netflix")
# writer.add_document(id=str(uuid.uuid4()), password='abcgbsk23', tags="email, wife")
# writer.add_document(id=str(uuid.uuid4()), password='abfaf', tags="Mi contra del febu")
# writer.commit()

word = "change"
# dbHandler.getPasswords(word)
dbHandler.getPasswords('')
# xd = dbHandler.searchPassword(word)
# dbHandler.updateDb(xd, "lecambielacontraseñapo")
# dbHandler.searchPassword(word)
# passwordIndex = dbHandler.index
# searcher = SearcherMenu(passwordIndex, word)
#
# a = searcher.run()


# dbHandler.searchPassword("Netfl~3")

# word = "net*"
# with passwordIndex.searcher() as searcher:
#     queryParser = QueryParser("tags", passwordIndex.schema)
#     queryParser.add_plugin(FuzzyTermPlugin())
#
#     query = queryParser.parse(word)
#     results = searcher.search(query)
#     for result in results:
#         print(type(result))
#         print(type(results))
