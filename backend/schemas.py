from whoosh.fields import Schema, ID, TEXT, KEYWORD

passwordSchema = Schema(
    id=ID(stored=True, unique=True, sortable=True),
    password=TEXT(stored=True),
    tags=KEYWORD(stored=True, commas=True)
)
