from datetime import datetime, timedelta
from whoosh.qparser import QueryParser

from ..globalVariables import USERNAME, VERIFY_TIME

# ===== Auxiliar Functions =====

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

        # Get time with verified password
        aux = master["verify_time"]
        limit = timedelta(minutes=aux)

        # Get currentTime, the last time that master password was used and compare them
        currentDate = datetime.now()
        lastTime = master["last_time"]

        # Get how much time remains
        timeAux = limit - (currentDate - lastTime)

        if timeAux.days == -1:
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
            user=master['user'],
            password=master['password'], 
            last_time=currentDate,
            verify_time=verifyTime
        )
        writer.commit()

# ===== Class Functions =====

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

        # Get time with verified password
        limitAux = master["verify_time"]
        limit = timedelta(minutes=limitAux)

        # Get currentTime, the last time that master password and max time limit
        currentDate = datetime.now()
        lastTime = master["last_time"]
        
        # Get how much time remains
        timeAux = limit - (currentDate - lastTime)
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

    # Encrypt password.
    _password = password

    # Get current date
    date = datetime.now()

    # Save in database
    writer.add_document(
        user=USERNAME,
        password=_password,
        last_time=date,
        verify_time=VERIFY_TIME
    )
    writer.commit()
