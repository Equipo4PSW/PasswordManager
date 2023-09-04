from whoosh.fields import Schema, ID, TEXT, KEYWORD, DATETIME, NUMERIC

passwordSchema = Schema(
    id=ID(stored=True, unique=True, sortable=True),
    password=TEXT(stored=True),
    tags=KEYWORD(stored=True, commas=True)
)

masterSchema = Schema(
    id=ID(stored=True, unique=True, sortable=True),
    user=TEXT(stored=True),
    password=TEXT(stored=True),
    last_time=DATETIME(stored=True),
    verify_time=NUMERIC(stored=True)
)
