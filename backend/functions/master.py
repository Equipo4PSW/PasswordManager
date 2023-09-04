from datetime import datetime, timedelta
from whoosh.qparser import QueryParser

from ..globalVariables import USERNAME, VERIFY_TIME, OK, NO_OK, NO_PASSWORD

# ===== Auxiliar Functions =====

def checkTime(self, on_screen=False) -> bool:
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

        # Check if there is a master password
        if len(results) == 0:
            print("Debes configurar una constraseña maestra antes de poder ejecutar cualquier otra funcion, para esto ejecuta: \n    python pm.py config")
            return NO_PASSWORD

        master = results[0]

        # Get time with verified password
        aux = master["verify_time"]
        limit = timedelta(minutes=aux)

        # Get currentTime, the last time that master password was used and compare them
        currentDate = datetime.now()
        lastTime = master["last_time"]

        # Get how much time remains
        timeAux = limit - (currentDate - lastTime)
        
        # Print remaining time
        if on_screen:
            min, sec = divmod(timeAux.seconds, 60)
            timeLeft = f"{min:02}:{sec:02}"

            if not timeAux.days == -1:
                print(f"Te quedan {timeLeft} de tener la clave maestra activa")
            else:
                print("No te queda tiempo activo con tu clave maestra, vuelve a ingresarla con: \n    python pm.py activate")

        if timeAux.days == -1:
            return NO_OK
        else:
            return OK


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


        # Ask for master password
        password = str(input("Ingrese la contraseña maestra: "))

        # Verify password
        # if not print"tamalo"

        # Get current time
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
    code = checkTime(self)

    if code == NO_OK:
        setNewVerifyTime(self, verifyTime)
        return True

    elif code == NO_PASSWORD:
        return False

    else:   
        return True

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
