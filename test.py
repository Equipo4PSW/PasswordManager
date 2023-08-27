from whoosh.qparser import QueryParser, FuzzyTermPlugin
from backend import Db

dbHandler = Db()

# TODO: Ojo si se spamea mucho el codigo, deja de agregar cosas, se podria testear cuando se complete el buscador.
dbHandler.addDb("abc123", ['Netflix', 'suegra'])
dbHandler.addDb("abc12345", ['Facebook', 'suegra'])
dbHandler.addDb("abcdb12345", ['mi contra del face'])

# writer = db.writerDB
# writer.add_document(id=str(uuid.uuid4()), password='abc123', tags="netflix, suegra")
# writer.add_document(id=str(uuid.uuid4()), password='abc123344', tags="face, suegra")
# writer.add_document(id=str(uuid.uuid4()), password='abcdas123', tags="youtube, suegra")
# writer.add_document(id=str(uuid.uuid4()), password='aaaaa123', tags="netflix")
# writer.add_document(id=str(uuid.uuid4()), password='abcgbsk23', tags="email, wife")
# writer.add_document(id=str(uuid.uuid4()), password='abfaf', tags="Mi contra del febu")
# writer.commit()

passwordIndex = dbHandler.index

# word = "net*"
word = "Netfl~3"
with passwordIndex.searcher() as searcher:
    queryParser = QueryParser("tags", passwordIndex.schema)
    queryParser.add_plugin(FuzzyTermPlugin())

    query = queryParser.parse(word)
    results = searcher.search(query)
    for result in results:
        print(result)
