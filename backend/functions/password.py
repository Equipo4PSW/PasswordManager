import uuid
import base64
from typing import List

from ..passwords import encrypter

# ===== Normal Passwords ======

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
    _passwordBytes = encrypter(password) 
    _password = base64.b64encode(_passwordBytes).decode('utf-8')

    # Save in database
    writer.add_document(id=_id, password=_password, tags=_tags)
    writer.commit()

    # TODO: Agregar un try: para ver si se guardo o no la contraseña.

def deleteDb(self, id: str):
    """
    Busca la por id la con contraseña deseada y la borra de la db

    Args:
        id (str): String con el id de la contraseña a borrar.
    """

    # Open writer for db
    writer = self.index.writer()

    # Delete element
    writer.delete_by_term("id", id)
    writer.commit()

def updateDb(self, obj:dict, password:str):
    """
    Busca la por id la con contraseña deseada y la actualiza.

    Args:
        id (str): String con el id de la contraseña a borrar.
        password (str): String con la contraseña sin decifrar.
    """

    # Open writer for db
    writer = self.index.writer()

    # Encrypt password.
    _passwordBytes = encrypter(password) 
    _password = base64.b64encode(_passwordBytes).decode('utf-8')

    # Update element
    writer.update_document(id=obj['id'], password=_password, tags=obj['tags'])
    writer.commit()

