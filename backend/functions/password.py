import uuid
import base64
import logging
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
    try:
        writer.add_document(id=_id, password=_password, tags=_tags)
        writer.commit()
        
        msg = "Se ha guardado correctamente la contraseña."
        print(msg)
        self.log.info(msg)
        
    except Exception as e:
        msg = f"Error al agregar contraseña a la base de datos: {str(e)}"
        print(msg)
        self.log.error(msg)


def deleteDb(self, id: str):
    """
    Busca la por id la con contraseña deseada y la borra de la db

    Args:
        id (str): String con el id de la contraseña a borrar.
    """

    # Open writer for db
    writer = self.index.writer()

    # Delete element
    try:
        writer.delete_by_term("id", id)
        writer.commit()

        msg = "Se ha borrado correctamente la contraseña."
        print(msg)
        self.log.info(msg)
        
    except Exception as e:
        msg = f"Error al borrar la contraseña en la base de datos: {str(e)}"
        print(msg)
        self.log.error(msg)

    # Delete element

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
    try:
        writer.update_document(id=obj['id'], password=_password, tags=obj['tags'])
        writer.commit()

        msg = "Se ha actualizado correctamente la contraseña."
        print(msg)
        self.log.info(msg)
        
    except Exception as e:
        msg = f"Error al actualizar la contraseña en la base de datos: {str(e)}"
        print(msg)
        self.log.error(msg)
