import uuid
from typing import List
from datetime import datetime, timedelta
from whoosh.qparser import QueryParser

USERNAME="user"
VERIFY_TIME = 5
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%M:%S"

# ===== General functions =====
# def verifyPassword()

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
    _password = password

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

    # Update element
    writer.update_document(id=obj['id'], password=password, tags=obj['tags'])
    writer.commit()

# ===== Master password =====
def getCurrentDate():
    """
    Obtiene la hora actual en el formato DATE_FORMAT definido anteriormente
    """

    # Get current time
    currentDate = datetime.now()

    # Format time in YYYY-MM-DD HH:DD:SS
    format = DATE_FORMAT
    date = currentDate.strftime(format)

    return date

def verifyToken(self) -> bool:
    """
    Verifica cuanto tiempo ha pasado desde la ultima vez que ingresamos la clave maestra.
    
    Retrun:
        bool: retorna si es posible o no seguir con cualquier accion.
    """
     
    with self.masterIndex.searcher() as searcher:
        # Get master password object
        queryParser = QueryParser("user", self.masterIndex.schema)
        query = queryParser.parse(USERNAME)
        results = searcher.search(query)
        master = results[0]

        # Get time with verify password
        aux = master["verify_time"]
        limit = timedelta(minutes=aux)

        # Get currentTime, the last time that master password was used and compare them
        # currentDate = getCurrentDate()
        currentDate = datetime.now()
        lastTime = master["last_time"]

        # date1 = datetime.strptime(currentDate, DATE_FORMAT)
        # date2 = datetime.strptime(lastTime, DATE_FORMAT)

        if currentDate-lastTime >= limit:
            return False
        else:
            return True

def setNewVerifyTime(self, verifyTime:int=VERIFY_TIME):
    """
    Realiza el proceso de definir una nueva fecha para definir cuanto tiempo puede
    estar activa la contraseña maestra.
    """
    
    with self.masterIndex.searcher() as searcher:
        # Get master password object
        queryParser = QueryParser("user", self.masterIndex.schema)
        query = queryParser.parse(USERNAME)
        results = searcher.search(query)
        master = results[0]

        # Get current time
        # currentDate = getCurrentDate()
        currentDate = datetime.now()

        # Open writer for db
        writer = self.masterIndex.writer()

        # Update element
        writer.update_document(
            id=master['id'], 
            user=master['user'],
            password=master['password'], 
            last_time=currentDate,
            verify_time=verifyTime
        )
        writer.commit()

def verifyHandler(self, verifyTime:int=VERIFY_TIME) -> bool:

    # Check time for master password
    if not verifyToken(self):

        # Ask for master password
        password = str(input("Ingrese la contraseña maestra: "))

        # Verify password
        # if not print"tamalo"

        setNewVerifyTime(self, verifyTime)

    return True

def checkTime(self):
    """
    Printea en pantalla cuanto tiempo tenemos con la contraseña maestra activada
    """

    with self.masterIndex.searcher() as searcher:
        # Get master password object
        queryParser = QueryParser("user", self.masterIndex.schema)
        query = queryParser.parse(USERNAME)
        results = searcher.search(query)
        master = results[0]

        # Get currentTime, the last time that master password and max time limit
        # currentDate = getCurrentDate()
        currentDate = datetime.now()
        lastTime = master["last_time"]

        limitAux = master["verify_time"]
        # limit = currentDate + timedelta(minutes=limitAux)
        limit = timedelta(minutes=limitAux)
    
        timeAux = limit - (currentDate - lastTime)
        # timeAux = lastTime - limit
        # timeLeft = timeAux.strftime(TIME_FORMAT)
        min, sec = divmod(timeAux.seconds, 60)
        timeLeft = f"{min:02}:{sec:02}"

        if not timeAux.days == -1:
            print(f"Te quedan {timeLeft} de tener la clave maestra activa")
        else:
            verifyHandler(self)

def addMasterDb(self, password: str):
    """
    Agrega la contraseña maestra cifrada a la base de datos y le asigna las tags relacionadas.

    Args:
        password (str): String con la contraseña sin decifrar.
    """

    # Search if there is a master password
    with self.masterIndex.searcher() as searcher:
        # Get master password object
        queryParser = QueryParser("user", self.masterIndex.schema)
        query = queryParser.parse(USERNAME)
        results = searcher.search(query)
        if not len(results) == 0:
            print("Ya tienes una contraseña maestra")
            return

    # Open writer for db
    writer = self.masterIndex.writer()

    # Gets an id
    _id = str(uuid.uuid4())

    # Encrypt password.
    _password = password

    # Get current date
    # date=getCurrentDate()
    date = datetime.now()

    # Save in database
    writer.add_document(
        id=_id,
        user=USERNAME,
        password=_password,
        last_time=date,
        verify_time=VERIFY_TIME
    )
    writer.commit()
