import uuid
from typing import List

def addDb(self, password: str, tagsList: List[str]):
    """
    Agrega la contraseña cifrada a la base de datos y le asigna las tags relacionadas.

    Args:
        password (str): String con la contraseña sin decifrar.
        tagsList (List[str]): Lista con todos los tags relacionados a la contraseña.
    """


    # Open writer for db
    writer = self.index.writer()

    # Gets an id
    _id = str(uuid.uuid4())
    
    # Gets a string of tags separated by commas.
    _tags = ",".join(tagsList)

    # Encrypt password.
    _password = password

    # Save in database
    writer.add_document(id=_id, password=_password, tags=_tags)
    writer.commit()
